import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Any


def parse_stock_page(url: str, symbol: str, logger: Any) -> pd.DataFrame:
    logger.info('Fetching URL for %s: %s', symbol, url)
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    logger.info('Parsing HTML for %s', symbol)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    if not table:
        logger.warning('Could not find <tbody> in HTML, attempting pandas fallback for %s', symbol)
        return parse_with_pandas(url, symbol, logger)

    rows = []
    for row in table.find_all('tr'):
        cols = [cell.text.strip() for cell in row.find_all('td')]
        if len(cols) >= 7:
            rows.append(cols[:7])

    if not rows:
        logger.warning('No rows were extracted from HTML table. Falling back to pandas for %s', symbol)
        return parse_with_pandas(url, symbol, logger)

    df = pd.DataFrame(rows, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    df['Symbol'] = symbol.upper()
    return df


def parse_with_pandas(url: str, symbol: str, logger: Any) -> pd.DataFrame:
    logger.info('Using pandas read_html fallback for %s', symbol)
    tables = pd.read_html(url)
    if not tables:
        raise ValueError(f'No tables found at URL: {url}')
    df = tables[0]
    if 'Date' not in df.columns:
        logger.warning('Pandas table does not include Date column for %s', symbol)
    df['Symbol'] = symbol.upper()
    return df

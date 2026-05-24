import time
import yfinance as yf
import pandas as pd
from typing import Any


def fetch_stock_data(symbol: str, period: str, logger: Any) -> pd.DataFrame:
    logger.info('Fetching %s from Yahoo Finance (period=%s)', symbol, period)
    last_exc: Exception = RuntimeError('Unknown error')
    for attempt in range(1, 4):
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            if not df.empty:
                break
            logger.warning('Empty response for %s on attempt %d', symbol, attempt)
        except Exception as exc:
            last_exc = exc
            logger.warning('Attempt %d failed for %s: %s', attempt, symbol, exc)
        if attempt < 3:
            time.sleep(2 ** attempt)
    else:
        raise ValueError(f'Failed to fetch data for {symbol} after 3 attempts') from last_exc

    if df.empty:
        raise ValueError(f'No data returned for symbol: {symbol}')

    df = df.reset_index()
    df['Symbol'] = symbol.upper()
    cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbol']
    return df[[c for c in cols if c in df.columns]]

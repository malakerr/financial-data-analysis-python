import pandas as pd
from typing import Any


def clean_stock_data(df: pd.DataFrame, logger: Any) -> pd.DataFrame:
    logger.info('Cleaning stock data with %d rows', len(df))
    result = df.copy()

    if 'Date' in result.columns:
        dates = pd.to_datetime(result['Date'], errors='coerce')
        if dates.dt.tz is not None:
            dates = dates.dt.tz_convert(None)
        result['Date'] = dates

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for column in numeric_columns:
        if column in result.columns:
            result[column] = (
                result[column]
                .astype(str)
                .str.replace(',', '', regex=False)
                .str.replace(r'^-$', '', regex=True)  # strip placeholder dashes, not minus signs
            )
            result[column] = pd.to_numeric(result[column], errors='coerce')

    result = result.dropna(subset=['Date'])
    available_numeric = [c for c in numeric_columns if c in result.columns]
    result = result.dropna(axis=0, how='all', subset=available_numeric)
    result = result.sort_values(by='Date').reset_index(drop=True)

    if result.empty:
        logger.warning('Cleaned dataframe is empty after cleaning.')
    else:
        logger.info('Cleaned dataframe contains %d rows', len(result))

    return result

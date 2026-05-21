import pandas as pd
from typing import Any


def add_analysis_columns(df: pd.DataFrame, logger: Any) -> pd.DataFrame:
    result = df.copy()
    if 'Close' not in result.columns:
        logger.warning('Close column missing; skipping analysis.')
        return result

    logger.info('Adding analysis columns')
    result['Daily Return'] = result['Close'].pct_change() * 100
    result['50-day MA'] = result['Close'].rolling(window=50, min_periods=1).mean()
    result['30-day Volatility'] = result['Daily Return'].rolling(window=30, min_periods=1).std()

    return result

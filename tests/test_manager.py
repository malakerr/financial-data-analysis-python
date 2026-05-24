import logging
import pandas as pd
import pytest
from scraper.manager import ScraperManager
from scraper.cleaning import clean_stock_data
from scraper.analysis import add_analysis_columns


def make_logger() -> logging.Logger:
    logger = logging.getLogger('test')
    logger.addHandler(logging.NullHandler())
    return logger


def make_manager(stocks=None):
    if stocks is None:
        stocks = [{'symbol': 'TEST', 'period': '1y'}]
    config = {'stocks': stocks, 'output': {}}
    return ScraperManager(config=config, logger=make_logger())


# --- ScraperManager.find_stock_config ---

def test_load_stock_config():
    manager = make_manager([{'symbol': 'TEST', 'period': '1y'}])
    stock_config = manager.find_stock_config('TEST')
    assert stock_config['symbol'] == 'TEST'


def test_find_stock_config_case_insensitive():
    manager = make_manager([{'symbol': 'NFLX', 'period': '1y'}])
    assert manager.find_stock_config('nflx')['symbol'] == 'NFLX'


def test_find_stock_config_missing_symbol_raises():
    manager = make_manager([{'symbol': 'AAPL', 'period': '1y'}])
    with pytest.raises(ValueError, match='GOOG'):
        manager.find_stock_config('GOOG')


def test_find_stock_config_empty_stocks_raises():
    manager = make_manager([])
    with pytest.raises(ValueError, match='No stocks configured'):
        manager.find_stock_config(None)


def test_find_stock_config_default_first():
    manager = make_manager([{'symbol': 'AAPL', 'period': '1y'}, {'symbol': 'MSFT', 'period': '1y'}])
    assert manager.find_stock_config(None)['symbol'] == 'AAPL'


# --- clean_stock_data ---

def make_raw_df(**kwargs):
    defaults = {
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Open': ['100', '101', '102'],
        'High': ['105', '106', '107'],
        'Low': ['99', '100', '101'],
        'Close': ['103', '104', '105'],
        'Volume': ['1000000', '1100000', '1200000'],
    }
    defaults.update(kwargs)
    return pd.DataFrame(defaults)


def test_clean_preserves_negative_numbers():
    df = make_raw_df(Close=['-1.50', '100', '101'])
    logger = make_logger()
    result = clean_stock_data(df, logger)
    assert result['Close'].iloc[0] == pytest.approx(-1.50)


def test_clean_converts_standalone_dash_to_nan():
    df = make_raw_df(Close=['-', '100', '101'])
    logger = make_logger()
    result = clean_stock_data(df, logger)
    assert pd.isna(result['Close'].iloc[0])


def test_clean_removes_comma_from_numbers():
    df = make_raw_df(Volume=['1,000,000', '1,100,000', '1,200,000'])
    logger = make_logger()
    result = clean_stock_data(df, logger)
    assert result['Volume'].iloc[0] == pytest.approx(1_000_000)


def test_clean_empty_dataframe_returns_empty():
    df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    logger = make_logger()
    result = clean_stock_data(df, logger)
    assert result.empty


def test_clean_drops_rows_with_invalid_date():
    df = make_raw_df(Date=['not-a-date', '2024-01-02', '2024-01-03'])
    logger = make_logger()
    result = clean_stock_data(df, logger)
    assert len(result) == 2


# --- add_analysis_columns ---

def make_clean_df(n=60):
    dates = pd.date_range('2023-01-01', periods=n, freq='B')
    prices = [100 + i * 0.5 for i in range(n)]
    return pd.DataFrame({'Date': dates, 'Close': prices, 'Volume': [1_000_000] * n})


def test_analysis_adds_expected_columns():
    df = make_clean_df()
    logger = make_logger()
    result = add_analysis_columns(df, logger)
    assert 'Daily Return' in result.columns
    assert 'Rolling_MA_50' in result.columns
    assert 'Rolling_Volatility_30' in result.columns


def test_analysis_missing_close_returns_unchanged():
    df = pd.DataFrame({'Date': pd.date_range('2024-01-01', periods=5, freq='B')})
    logger = make_logger()
    result = add_analysis_columns(df, logger)
    assert 'Rolling_MA_50' not in result.columns

import os
from typing import Any, Dict, Optional
import pandas as pd
from scraper.parser import fetch_stock_data
from scraper.cleaning import clean_stock_data
from scraper.storage import save_csv, save_json, save_sqlite
from scraper.analysis import add_analysis_columns
from scraper.visualization import save_price_plot
from scraper.utils import current_timestamp


class ScraperManager:
    def __init__(self, config: Dict[str, Any], logger: Any) -> None:
        self.config = config
        self.logger = logger

    def find_stock_config(self, symbol: Optional[str]) -> Dict[str, Any]:
        stocks = self.config.get('stocks', [])
        if symbol:
            symbol_upper = symbol.strip().upper()
            for stock in stocks:
                if stock.get('symbol', '').upper() == symbol_upper:
                    return stock
            raise ValueError(f'Stock symbol not found in config: {symbol}')
        if stocks:
            return stocks[0]
        raise ValueError('No stocks configured in config.yaml')

    def run(self, stock_symbol: Optional[str] = None, output_option: str = 'all', run_analysis: bool = True) -> None:
        stock_config = self.find_stock_config(stock_symbol)
        symbol = stock_config['symbol']
        period = stock_config.get('period', '5y')

        self.logger.info('Starting pipeline for %s', symbol)
        raw_df = fetch_stock_data(symbol, period, logger=self.logger)

        raw_folder = self.config.get('output', {}).get('raw_folder', 'data/raw')
        self._save_dataframe(raw_df, raw_folder, f'{symbol}_raw_{current_timestamp()}.csv')

        cleaned_df = clean_stock_data(raw_df, logger=self.logger)
        clean_folder = self.config.get('output', {}).get('clean_folder', 'data/clean')
        self._save_dataframe(cleaned_df, clean_folder, f'{symbol}_clean_{current_timestamp()}.csv')

        if output_option in ('csv', 'all'):
            save_csv(cleaned_df, symbol, self.config, logger=self.logger)
        if output_option in ('json', 'all'):
            save_json(cleaned_df, symbol, self.config, logger=self.logger)
        if output_option in ('sqlite', 'all') and self.config.get('output', {}).get('sqlite', False):
            save_sqlite(cleaned_df, symbol, self.config, logger=self.logger)

        if run_analysis:
            analysis_df = add_analysis_columns(cleaned_df, logger=self.logger)
            chart_path = save_price_plot(analysis_df, symbol, self.config, logger=self.logger)
            self.logger.info('Saved chart: %s', chart_path)

        self.logger.info('Pipeline completed for %s', symbol)

    def _save_dataframe(self, df: pd.DataFrame, folder: str, filename: str) -> str:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        df.to_csv(path, index=False)
        self.logger.info('Saved data to %s', path)
        return path

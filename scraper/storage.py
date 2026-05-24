import os
import json
import sqlite3
import pandas as pd
from typing import Any, Dict
from scraper.utils import current_timestamp


def save_csv(df: pd.DataFrame, symbol: str, config: Dict[str, Any], logger: Any) -> str:
    folder = config.get('output', {}).get('output_folder', 'data/output')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{symbol}_clean_{current_timestamp()}.csv')
    df.to_csv(path, index=False)
    logger.info('Saved CSV output to %s', path)
    return path


def save_json(df: pd.DataFrame, symbol: str, config: Dict[str, Any], logger: Any) -> str:
    folder = config.get('output', {}).get('output_folder', 'data/output')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{symbol}_clean_{current_timestamp()}.json')
    df.to_json(path, orient='records', date_format='iso')
    logger.info('Saved JSON output to %s', path)
    return path


def save_sqlite(df: pd.DataFrame, symbol: str, config: Dict[str, Any], logger: Any) -> str:
    db_path = config.get('output', {}).get('sqlite_path', 'data/db/scraper_data.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    table_name = symbol.lower()
    with sqlite3.connect(db_path) as connection:
        df.to_sql(table_name, connection, if_exists='replace', index=False)
    logger.info('Saved SQLite output to %s (table: %s)', db_path, table_name)
    return db_path

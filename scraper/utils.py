import logging
import os
from datetime import datetime


def setup_logging(log_path: str) -> logging.Logger:
    dir_name = os.path.dirname(log_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    logger = logging.getLogger('scraper')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def current_timestamp() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S')

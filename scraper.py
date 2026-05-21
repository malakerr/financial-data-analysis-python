import argparse
from importlib.resources import path
import yaml
from scraper.manager import ScraperManager
from scraper.utils import setup_logging


def load_config(path: str) -> dict:
    """
    Converts YAML config file into a Python dictionary

    Parameters:
        path (str): Path to the YAML config file

    Returns:
        dict: The loaded configuration as a Python dictionary
    """
    with open(path, 'r', encoding='utf-8') as config_file:
        return yaml.safe_load(config_file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Run the stock data scraper pipeline.'
    )
    parser.add_argument('--config', default='config.yaml', help='Path to YAML config file.')
    parser.add_argument('--stock', help='Stock symbol to scrape. Overrides config if provided.')
    parser.add_argument('--output', choices=['csv', 'json', 'sqlite', 'all'], default='all', help='Output format for scraped data.')
    parser.add_argument('--no-analysis', action='store_true', help='Skip analysis and visualization steps.')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    logger = setup_logging(config.get('output', {}).get('log_file', 'logs/scraper.log'))

    manager = ScraperManager(config=config, logger=logger)
    manager.run(
        stock_symbol=args.stock,
        output_option=args.output,
        run_analysis=not args.no_analysis,
    )


if __name__ == '__main__':
    main()

import yaml
from scraper.manager import ScraperManager


def test_load_stock_config():
    config = {
        'stocks': [
            {'symbol': 'TEST', 'url': 'https://example.com'}
        ],
        'output': {}
    }
    manager = ScraperManager(config=config, logger=None)
    stock_config = manager.find_stock_config('TEST')
    assert stock_config['symbol'] == 'TEST'
    assert stock_config['url'] == 'https://example.com'

import os
import matplotlib.pyplot as plt
from typing import Any, Dict


def save_price_plot(df, symbol: str, config: Dict[str, Any], logger: Any) -> str:
    folder = config.get('output', {}).get('output_folder', 'data/output')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{symbol}_close_plot.png')

    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price', marker='o', markersize=3)
    if '50-day MA' in df.columns:
        plt.plot(df['Date'], df['50-day MA'], label='50-day MA', linewidth=1)
    plt.title(f'{symbol} Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    logger.info('Saved visualization to %s', path)
    return path

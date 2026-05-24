import os
import matplotlib.pyplot as plt
from typing import Any, Dict


def save_price_plot(df, symbol: str, config: Dict[str, Any], logger: Any) -> str:
    folder = config.get('output', {}).get('output_folder', 'data/output')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{symbol}_close_plot.png')

    has_volume = 'Volume' in df.columns
    if has_volume:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                        gridspec_kw={'height_ratios': [3, 1]})
    else:
        fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(df['Date'], df['Close'], label='Close Price')
    if 'Rolling_MA_50' in df.columns:
        ax1.plot(df['Date'], df['Rolling_MA_50'], label='50-day MA', linewidth=1)
    ax1.set_title(f'{symbol} Close Price')
    ax1.set_ylabel('Price (USD)')
    ax1.legend()
    ax1.grid(True)

    if has_volume:
        ax2.bar(df['Date'], df['Volume'], label='Volume', alpha=0.5, width=1)
        ax2.set_ylabel('Volume')
        ax2.legend()

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    logger.info('Saved visualization to %s', path)
    return path

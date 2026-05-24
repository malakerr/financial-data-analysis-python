# Financial Data Analysis Pipeline

A modular Python pipeline that fetches stock data from Yahoo Finance, cleans and validates it, runs financial analysis, and produces charts and structured output files.

---

## Project Structure

```
financial-data-analysis-python/
├── scraper.py               # CLI entry point
├── config.yaml              # Stock symbols and output settings
├── requirements.txt
├── scraper/
│   ├── __init__.py
│   ├── manager.py           # Orchestrates the full pipeline
│   ├── parser.py            # Fetches data from Yahoo Finance
│   ├── cleaning.py          # Cleans and validates the raw DataFrame
│   ├── analysis.py          # Adds derived columns (returns, moving averages, volatility)
│   ├── visualization.py     # Generates and saves price + volume charts
│   ├── storage.py           # Writes CSV, JSON, and SQLite outputs
│   └── utils.py             # Logging setup and shared utilities
├── tests/
│   └── test_manager.py
├── data/
│   ├── raw/                 # Timestamped raw data snapshots
│   ├── clean/               # Timestamped cleaned data
│   └── output/              # Final CSV, JSON, and chart files
└── logs/
    └── scraper.log
```

---

## Pipeline Steps

1. **Fetch** — Downloads historical OHLCV data from Yahoo Finance using `yfinance`. Retries up to 3 times on failure.
2. **Clean** — Parses dates, strips formatting characters, converts columns to numeric types, and drops invalid rows.
3. **Analyze** — Adds `Daily Return`, `Rolling_MA_50` (50-day rolling mean), and `Rolling_Volatility_30` (30-day rolling standard deviation).
4. **Visualize** — Saves a two-panel PNG chart: close price with the 50-day moving average on top, and a volume bar chart below.
5. **Store** — Writes timestamped CSV and JSON files to `data/output/`. Optionally writes to a SQLite database.

---

## Tech Stack

| Concern | Library |
|---|---|
| Data fetching | yfinance |
| Data manipulation | pandas |
| Visualization | matplotlib |
| Configuration | PyYAML |
| Testing | pytest |
| CI | GitHub Actions |

---

## Setup

**Requirements:** Python 3.10 or later.

```powershell
# Create and activate a virtual environment (Windows)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

Run the pipeline with default settings (fetches NFLX, outputs CSV and JSON):

```powershell
python scraper.py
```

**Options:**

```
--config PATH       Path to a YAML config file (default: config.yaml)
--stock SYMBOL      Stock symbol to run. Must be listed in config.yaml.
--output FORMAT     Output format: csv, json, sqlite, or all (default: all)
--no-analysis       Skip analysis and chart generation
```

**Examples:**

```powershell
# Run for a specific symbol
python scraper.py --stock NFLX

# CSV output only, skip chart
python scraper.py --stock NFLX --output csv --no-analysis

# Use a custom config file
python scraper.py --config myconfig.yaml
```

---

## Configuration

`config.yaml` controls which stocks to fetch and where outputs are written.

```yaml
stocks:
  - symbol: NFLX
    period: 5y        # Any period accepted by yfinance: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

output:
  csv: true
  json: true
  sqlite: false
  output_folder: data/output
  raw_folder: data/raw
  clean_folder: data/clean
  sqlite_path: data/db/scraper_data.db
  save_charts: true
  log_file: logs/scraper.log
```

To add more stocks, append entries to the `stocks` list. The `--stock` flag selects which one to run; without it, the first entry is used.

---

## Output Files

All output filenames include a timestamp to prevent silent overwrites.

| Location | Contents |
|---|---|
| `data/raw/NFLX_raw_<timestamp>.csv` | Raw data as returned by Yahoo Finance |
| `data/clean/NFLX_clean_<timestamp>.csv` | Cleaned and validated data |
| `data/output/NFLX_clean_<timestamp>.csv` | Final CSV for downstream use |
| `data/output/NFLX_clean_<timestamp>.json` | Final JSON for downstream use |
| `data/output/NFLX_close_plot.png` | Price and volume chart |
| `logs/scraper.log` | Full run log |

---

## Tests

```powershell
python -m pytest tests/ -v
```

The test suite covers `ScraperManager` config resolution, cleaning edge cases (negative numbers, placeholder dashes, comma-formatted numbers, empty DataFrames, invalid dates), and analysis column generation. Tests run automatically on every push via GitHub Actions.

---

## CI

A GitHub Actions workflow at `.github/workflows/tests.yml` installs dependencies and runs the test suite on every push and pull request to `main`.

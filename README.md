# Finance — Simple SMA Crossover Backtester

**Purpose:** Minimal, effective finance project you can upload to GitHub.  
The repo contains a small Python app that downloads historical price data (via `yfinance`), runs a simple SMA crossover strategy backtest, outputs performance metrics, and saves charts.

## Contents
- `main.py` — CLI entry point to run backtests and save outputs.
- `strategy.py` — Backtesting logic (SMA crossover) and performance metrics.
- `requirements.txt` — Python dependencies.
- `.gitignore`
- `README.md` — this file.

## Quick start (on your machine)
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS / Linux
   venv\Scripts\activate     # Windows PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the example backtest (AAPL, last 3 years):
   ```bash
   python main.py --ticker AAPL --period "3y" --fast 20 --slow 50
   ```
4. Outputs:
   - `outputs/` directory with `equity_curve.png`, `price_with_signals.png`, and `metrics.json`.

## To push to GitHub
```bash
git init
git add .
git commit -m "Initial: simple SMA crossover backtester"
gh repo create your-repo-name --public --source=. --remote=origin --push
```
*(I cannot push to your GitHub account — you must run the commands above yourself or share a token in your environment.)*

## Notes (brutally honest)
- This is a **learning/demo** project, not production trading software.
- It does not include execution, slippage, transaction costs beyond a simple fee placeholder.
- Use responsibly. Backtest results do not guarantee future returns.

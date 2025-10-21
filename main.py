"""CLI entrypoint for the SMA crossover backtester.

Example:
    python main.py --ticker AAPL --period 3y --fast 20 --slow 50
"""
import argparse
import os
import json
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from strategy import generate_signals, backtest

OUTPUT_DIR = 'outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_price_with_signals(df, ticker, outpath):
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df['Close'], label='Close')
    plt.plot(df.index, df['sma_fast'], label='SMA_fast')
    plt.plot(df.index, df['sma_slow'], label='SMA_slow')
    # mark entries/exits
    buys = df[df['positions']>0]
    sells = df[df['positions']<0]
    plt.scatter(buys.index, buys['Close'], marker='^', label='Buy', s=80)
    plt.scatter(sells.index, sells['Close'], marker='v', label='Sell', s=80)
    plt.title(f'{ticker} Price & SMA signals')
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def plot_equity_curve(df, outpath):
    plt.figure(figsize=(10,5))
    plt.plot(df.index, df['equity'], label='Equity')
    plt.title('Equity Curve')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def run_backtest(ticker='AAPL', period='3y', fast=20, slow=50, initial_capital=10000):
    print(f"Downloading {ticker} historical data for period={period} ...")
    data = yf.download(ticker, period=period, progress=False)
    if data.empty:
        raise SystemExit("No data downloaded. Check ticker/period and your internet connection.")
    df = generate_signals(data, fast=fast, slow=slow)
    bt_df, metrics = backtest(df, initial_capital=initial_capital)
    # save outputs
    price_path = os.path.join(OUTPUT_DIR, f'{ticker}_price_signals.png')
    equity_path = os.path.join(OUTPUT_DIR, f'{ticker}_equity_curve.png')
    metrics_path = os.path.join(OUTPUT_DIR, f'{ticker}_metrics.json')

    plot_price_with_signals(bt_df, ticker, price_path)
    plot_equity_curve(bt_df, equity_path)

    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    print('Backtest complete. Outputs saved to', OUTPUT_DIR)
    return metrics

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple SMA crossover backtester')
    parser.add_argument('--ticker', type=str, default='AAPL')
    parser.add_argument('--period', type=str, default='3y')
    parser.add_argument('--fast', type=int, default=20)
    parser.add_argument('--slow', type=int, default=50)
    parser.add_argument('--capital', type=float, default=10000)
    args = parser.parse_args()
    metrics = run_backtest(args.ticker, args.period, args.fast, args.slow, args.capital)
    print(json.dumps(metrics, indent=2))

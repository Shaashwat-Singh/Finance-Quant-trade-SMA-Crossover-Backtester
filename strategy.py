# strategy.py
import pandas as pd
import numpy as np

def compute_sma(df, window, price_col='Close'):
    """Compute simple moving average with minimal periods."""
    return df[price_col].rolling(window, min_periods=1).mean()

def generate_signals(df, fast=20, slow=50):
    """
    Generate trading signals based on SMA crossover.
    signal = 1 when fast SMA > slow SMA, else 0
    """
    df = df.copy()
    df['sma_fast'] = compute_sma(df, fast)
    df['sma_slow'] = compute_sma(df, slow)
    df['signal'] = np.where(df['sma_fast'] > df['sma_slow'], 1, 0)
    df['positions'] = df['signal'].diff().fillna(0)
    return df

def backtest(df, initial_capital=10000.0, fee=0.0):
    """
    Simple SMA crossover backtest.
    All-in/all-out strategy with optional transaction fee.
    """
    df = df.copy().reset_index()
    cash = initial_capital
    shares = 0
    equity_curve = []

    for i in range(len(df)):
        # Force scalar extraction
        price = float(df.loc[i, 'Close'])
        signal = int(df.loc[i, 'signal'])

        # BUY
        if signal == 1 and shares == 0:
            max_shares = int(cash // (price * (1 + fee)))
            if max_shares > 0:
                shares = max_shares
                cash -= shares * price * (1 + fee)

        # SELL
        elif signal == 0 and shares > 0:
            cash += shares * price * (1 - fee)
            shares = 0

        # Track equity
        equity = cash + shares * price
        equity_curve.append(equity)

    df['equity'] = equity_curve

    # ---- Performance metrics ----
    returns = pd.Series(equity_curve).pct_change().fillna(0)
    total_return = (df['equity'].iloc[-1] / initial_capital) - 1

    annualized_return = (1 + total_return) ** (252 / len(df)) - 1
    annualized_vol = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else np.nan

    metrics = {
        'initial_capital': initial_capital,
        'final_equity': df['equity'].iloc[-1],
        'total_return': total_return,
        'annualized_return': annualized_return,
        'annualized_vol': annualized_vol,
        'sharpe': sharpe,
    }

    if 'Date' in df.columns:
        df = df.set_index('Date')

    return df, metrics

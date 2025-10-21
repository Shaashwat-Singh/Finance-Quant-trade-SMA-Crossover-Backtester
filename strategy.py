import pandas as pd
import numpy as np

def compute_sma(df, window, price_col='Close'):
    return df[price_col].rolling(window, min_periods=1).mean()

def generate_signals(df, fast=20, slow=50):
    df = df.copy()
    df['sma_fast'] = compute_sma(df, fast)
    df['sma_slow'] = compute_sma(df, slow)
    # signal: 1 for long, 0 for flat
    df['signal'] = 0
    df.loc[df['sma_fast'] > df['sma_slow'], 'signal'] = 1
    # generate trades: when signal changes
    df['positions'] = df['signal'].diff().fillna(0)
    return df

def backtest(df, initial_capital=10000.0, fee=0.0):
    df = df.copy().reset_index()
    # We'll assume we go all-in when long, fully out when flat
    capital = initial_capital
    positions = 0.0
    equity_curve = []
    cash = capital
    shares = 0.0

    for idx, row in df.iterrows():
        price = row['Close']
        signal = row['signal']
        if idx==0:
            equity = capital
        # Enter long
        if signal == 1 and shares == 0:
            # buy as many shares as possible
            shares = (cash * (1 - fee)) // price
            cash -= shares * price * (1 + fee)
        # Exit to cash
        elif signal == 0 and shares > 0:
            cash += shares * price * (1 - fee)
            shares = 0
        equity = cash + shares * price
        equity_curve.append(equity)

    df['equity'] = equity_curve
    # metrics
    returns = pd.Series(equity_curve).pct_change().fillna(0)
    total_return = (equity_curve[-1] / initial_capital) - 1
    annualized_return = (1 + total_return) ** (252.0 / len(df)) - 1 if len(df)>0 else 0.0
    annualized_vol = returns.std() * (252 ** 0.5)
    sharpe = (returns.mean() / returns.std()) * (252 ** 0.5) if returns.std() != 0 else float('nan')

    metrics = {
        'initial_capital': initial_capital,
        'final_equity': equity_curve[-1] if len(equity_curve)>0 else initial_capital,
        'total_return': total_return,
        'annualized_return': annualized_return,
        'annualized_vol': annualized_vol,
        'sharpe': sharpe
    }
    return df.set_index('Date'), metrics

import pandas as pd
import numpy as np

# Calculate Volatility (Annualized standard deviation of daily returns)
def calculate_volatility(df):
    # Use 'Close' instead of 'Adj Close' for volatility calculation
    daily_returns = df['Close'].pct_change()
    volatility = daily_returns.std() * (252 ** 0.5)  # Annualized volatility
    return volatility


# Calculate Maximum Drawdown
def calculate_max_drawdown(df):
    rolling_max = df['Close'].cummax()
    drawdown = (df['Close'] - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    return max_drawdown

# Calculate Moving Averages
def calculate_moving_averages(df):
    ma_30 = df['Close'].rolling(window=30).mean()
    ma_180 = df['Close'].rolling(window=180).mean()
    ma_365 = df['Close'].rolling(window=365).mean()
    return ma_30.iloc[-1], ma_180.iloc[-1], ma_365.iloc[-1]

# Function to calculate all metrics for a stock
def calculate_metrics(stock_df):
    volatility = calculate_volatility(stock_df)
    max_drawdown = calculate_max_drawdown(stock_df)
    ma_30, ma_180, ma_365 = calculate_moving_averages(stock_df)
    
    return {
        'volatility': volatility,
        'max_drawdown': max_drawdown,
        'ma_30': ma_30,
        'ma_180': ma_180,
        'ma_365': ma_365
    }

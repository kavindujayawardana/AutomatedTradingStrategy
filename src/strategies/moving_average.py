import pandas as pd

def moving_average_crossover(df: pd.DataFrame, short_window: int = 20, long_window: int = 50):
    """
    Implements Moving Average Crossover strategy.
    Returns DataFrame with buy/sell signals.
    """
    df = df.copy()
    df["SMA_short"] = df["close"].rolling(window=short_window).mean()
    df["SMA_long"] = df["close"].rolling(window=long_window).mean()

    df["signal"] = 0
    df.loc[df["SMA_short"] > df["SMA_long"], "signal"] = 1   # Buy
    df.loc[df["SMA_short"] < df["SMA_long"], "signal"] = -1  # Sell
    df["positions"] = df["signal"].diff()

    return df
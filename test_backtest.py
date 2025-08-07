import pandas as pd
from src.backtesting.backtester import Backtester

# Load data
df = pd.read_csv("data/sample_prices.csv")  # has Date, Close
df['MA3'] = df['Close'].rolling(window=3).mean()
df['Signal'] = 0
df.loc[df['Close'] > df['MA3'], 'Signal'] = 1
df.loc[df['Close'] < df['MA3'], 'Signal'] = -1

# Run backtester
bt = Backtester(df)
result_df = bt.run()
metrics = bt.metrics()
bh_return = bt.buy_and_hold_return()

# Print results
print("Backtest Metrics:")
for k, v in metrics.items():
    print(f"{k}: {v}")
print(f"Buy & Hold Return: {bh_return:.2%}")

import matplotlib.pyplot as plt
plt.plot(result_df['Date'], result_df['Portfolio'])
plt.title("Portfolio Value Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

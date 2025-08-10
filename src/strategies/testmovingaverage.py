import pandas as pd
from src.strategies.moving_average import moving_average_crossover

data = {"close": [10, 11, 12, 13, 12, 11, 10, 9, 8, 9, 10]}
df = pd.DataFrame(data)

df = moving_average_crossover(df, 3, 5)
print(df.tail())
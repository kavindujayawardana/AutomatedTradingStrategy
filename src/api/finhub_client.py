import finnhub
import pandas as pd
import os

class FinnhubClient:
    def __init__(self, api_key: str):
        self.client = finnhub.Client(api_key=api_key)

    def get_historical_data(self, symbol: str, resolution: str = "D", start: int = None, end: int = None):
        """
        Fetch historical OHLCV data from Finnhub.
        resolution: "1", "5", "15", "30", "60", "D", "W", "M"
        """
        data = self.client.stock_candles(symbol, resolution, start, end)

        if data.get("s") != "ok":
            raise ValueError(f"Error fetching data: {data}")

        df = pd.DataFrame(data)
        df["t"] = pd.to_datetime(df["t"], unit="s")
        df.rename(columns={
            "t": "time", "o": "open", "h": "high",
            "l": "low", "c": "close", "v": "volume"
        }, inplace=True)

        return df[["time", "open", "high", "low", "close", "volume"]]
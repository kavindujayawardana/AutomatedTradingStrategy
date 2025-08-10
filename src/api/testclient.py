from finhub_client import FinnhubClient
import os
from datetime import datetime, timedelta

# Load API key from environment
api_key = os.getenv("FINNHUB_API_KEY")

client = FinnhubClient(api_key)

end = int(datetime.now().timestamp())
start = int((datetime.now() - timedelta(days=365)).timestamp())

df = client.get_historical_data("AAPL", "D", start, end)
print(df.head())
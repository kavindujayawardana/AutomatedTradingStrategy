import pandas as pd
import numpy as np
import pytest
from src.backtesting.backtester import Backtester

# Fixture: create a small dummy dataframe
@pytest.fixture
def sample_data():
    df = pd.DataFrame({
        'Date': pd.date_range(start='2022-01-01', periods=7),
        'Close': [100, 102, 104, 103, 105, 107, 110],
    })
    df['MA3'] = df['Close'].rolling(window=3).mean()
    df['Signal'] = 0
    df.loc[df['Close'] > df['MA3'], 'Signal'] = 1
    df.loc[df['Close'] < df['MA3'], 'Signal'] = -1
    return df

def test_run_returns_dataframe(sample_data):
    bt = Backtester(sample_data)
    result = bt.run()
    assert isinstance(result, pd.DataFrame), "Backtester run() should return a DataFrame"
    assert 'Portfolio' in result.columns, "Output DataFrame must include 'Portfolio' column"

def test_metrics_keys_exist(sample_data):
    bt = Backtester(sample_data)
    bt.run()
    metrics = bt.metrics()
    expected_keys = ['Total Return', 'Sharpe Ratio', 'Max Drawdown', 'Profit Factor', 'Win Rate']
    for key in expected_keys:
        assert key in metrics, f"{key} not found in metrics output"

def test_buy_and_hold(sample_data):
    bt = Backtester(sample_data)
    bh_return = bt.buy_and_hold_return()
    expected = (sample_data['Close'].iloc[-1] / sample_data['Close'].iloc[0]) - 1
    np.testing.assert_almost_equal(bh_return, expected, decimal=6)

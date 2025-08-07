import numpy as np


class Backtester:
    def __init__(self, df, initial_cash=10000):
        """
        df should have: ['Date', 'Close', 'Signal']
        Signal = 1 (buy), -1 (sell), 0 (hold)
        """
        self.df = df.copy()
        self.initial_cash = initial_cash
        self.df['Position'] = 0
        self.df['Cash'] = initial_cash
        self.df['Portfolio'] = initial_cash
        self.trades = []

    def run(self):
        position = 0
        cash = self.initial_cash

        for i in range(1, len(self.df)):
            signal = self.df.loc[i, 'Signal']
            price = self.df.loc[i, 'Close']

            # BUY
            if signal == 1 and cash >= price:
                position = cash // price
                cash -= position * price
                self.trades.append(('Buy', self.df.loc[i, 'Date'], price))

            # SELL
            elif signal == -1 and position > 0:
                cash += position * price
                self.trades.append(('Sell', self.df.loc[i, 'Date'], price))
                position = 0

            self.df.loc[i, 'Position'] = position
            self.df.loc[i, 'Cash'] = cash
            self.df.loc[i, 'Portfolio'] = cash + position * price

        return self.df

    def metrics(self):
        self.df['Returns'] = self.df['Portfolio'].pct_change().fillna(0)
        total_return = (self.df['Portfolio'].iloc[-1] / self.initial_cash) - 1
        sharpe = np.mean(self.df['Returns']) / np.std(self.df['Returns']) * np.sqrt(252)
        max_dd = self.df['Portfolio'].div(self.df['Portfolio'].cummax()).sub(1).min()
        profit_factor = self._profit_factor()
        win_rate = self._win_rate()

        return {
            'Total Return': f'{total_return:.2%}',
            'Sharpe Ratio': round(sharpe, 2),
            'Max Drawdown': f'{max_dd:.2%}',
            'Profit Factor': round(profit_factor, 2),
            'Win Rate': f'{win_rate:.2%}'
        }

    def _profit_factor(self):
        profits, losses = [], []
        for i in range(1, len(self.trades), 2):
            if i < len(self.trades):
                buy_price = self.trades[i-1][2]
                sell_price = self.trades[i][2]
                pl = sell_price - buy_price
                if pl > 0:
                    profits.append(pl)
                else:
                    losses.append(abs(pl))
        return sum(profits) / sum(losses) if losses else float('inf')

    def _win_rate(self):
        wins, total = 0, 0
        for i in range(1, len(self.trades), 2):
            if i < len(self.trades):
                buy_price = self.trades[i-1][2]
                sell_price = self.trades[i][2]
                if sell_price > buy_price:
                    wins += 1
                total += 1
        return wins / total if total > 0 else 0

    def buy_and_hold_return(self):
        first = self.df['Close'].iloc[0]
        last = self.df['Close'].iloc[-1]
        return (last / first) - 1

import alpaca_trade_api as tradeapi
import pandas as pd
import os

class Backtester:
    def __init__(self, start_date, end_date):
        self.api = tradeapi.REST(
            os.getenv('APCA_API_KEY_ID'),
            os.getenv('APCA_API_SECRET_KEY'),
            os.getenv('APCA_API_BASE_URL', 'https://paper-api.alpaca.markets'),
            api_version='v2'
        )
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = 10000  # Starting with a fixed initial capital for simulation
        self.portfolio_value = self.initial_capital
        self.positions = {}
        self.trades = []

    def run(self, symbol):
        """
        Runs the backtest for a given symbol.
        """
        print(f"Running backtest for {symbol} from {self.start_date} to {self.end_date}...")

        # Fetch historical data
        historical_data = self.api.get_bars(
            symbol,
            '1Day',
            start=self.start_date,
            end=self.end_date
        ).df

        # Calculate moving averages
        historical_data['short_mavg'] = historical_data['close'].rolling(window=50).mean()
        historical_data['long_mavg'] = historical_data['close'].rolling(window=200).mean()

        # Simulate the strategy
        for i in range(1, len(historical_data)):
            # Buy signal
            if historical_data['short_mavg'].iloc[i] > historical_data['long_mavg'].iloc[i] and \
               historical_data['short_mavg'].iloc[i-1] <= historical_data['long_mavg'].iloc[i-1]:
                self.execute_trade(symbol, 'buy', historical_data['close'].iloc[i])

            # Sell signal
            elif historical_data['short_mavg'].iloc[i] < historical_data['long_mavg'].iloc[i] and \
                 historical_data['short_mavg'].iloc[i-1] >= historical_data['long_mavg'].iloc[i-1]:
                self.execute_trade(symbol, 'sell', historical_data['close'].iloc[i])

        print("Backtest complete.")
        return self.get_results()

    def execute_trade(self, symbol, side, price):
        """
        Simulates executing a trade.
        """
        if side == 'buy':
            # Simplified: invest a fixed portion of capital
            investment_size = self.initial_capital * 0.1
            quantity = investment_size / price
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
            self.portfolio_value -= quantity * price
            self.trades.append(f"BOUGHT {quantity:.2f} of {symbol} at ${price:.2f}")

        elif side == 'sell' and self.positions.get(symbol, 0) > 0:
            quantity = self.positions[symbol]
            self.portfolio_value += quantity * price
            self.positions[symbol] = 0
            self.trades.append(f"SOLD {quantity:.2f} of {symbol} at ${price:.2f}")

    def get_results(self):
        """
        Returns the results of the backtest.
        """
        final_portfolio_value = self.portfolio_value
        # Add current value of open positions
        for symbol, quantity in self.positions.items():
            latest_price = self.api.get_latest_trade(symbol).price
            final_portfolio_value += quantity * latest_price

        return {
            "initial_capital": self.initial_capital,
            "final_portfolio_value": final_portfolio_value,
            "profit_loss": final_portfolio_value - self.initial_capital,
            "trades": self.trades
        }

if __name__ == '__main__':
    # Example usage:
    backtester = Backtester(start_date='2022-01-01', end_date='2023-01-01')
    results = backtester.run(symbol='AAPL')
    print(results)

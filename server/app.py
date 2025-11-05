import os
import alpaca_trade_api as tradeapi
from flask import Flask, request, jsonify
import pandas as pd
import threading
import time
from backtester import Backtester

app = Flask(__name__)

# --- Alpaca API Configuration ---
api = tradeapi.REST(
    os.getenv('APCA_API_KEY_ID'),
    os.getenv('APCA_API_SECRET_KEY'),
    os.getenv('APCA_API_BASE_URL', 'https://paper-api.alpaca.markets'),
    api_version='v2'
)

# --- Trading Bot Class ---
class TradingBot:
    def __init__(self):
        self.running = False
        self.thread = None
        self.portfolio_value = 0
        self.recent_trades = []
        self.lock = threading.Lock()

    def get_signal(self, symbol):
        """Generates a trading signal."""
        try:
            barset = api.get_bars(symbol, '1Day', limit=200).df
            close_prices = barset['close']
            short_mavg = close_prices.rolling(window=50).mean()
            long_mavg = close_prices.rolling(window=200).mean()
            return 'buy' if short_mavg.iloc[-1] > long_mavg.iloc[-1] else 'sell'
        except Exception as e:
            print(f"Error getting signal for {symbol}: {e}")
            return None

    def trading_loop(self, investment_amount, risk_level, target_roi, timeframe):
        """The main trading loop."""
        print(f"Trading loop started with target ROI: {target_roi}% over {timeframe}.")
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        while self.running:
            for symbol in symbols:
                if not self.running:
                    break
                signal = self.get_signal(symbol)

                if signal == 'buy':
                    try:
                        quantity = (investment_amount * (risk_level / 100)) / api.get_latest_trade(symbol).price
                        api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
                        self.record_trade(f"BOUGHT {quantity:.2f} of {symbol}")
                    except Exception as e:
                        print(f"Error buying {symbol}: {e}")
                elif signal == 'sell':
                    try:
                        position = api.get_position(symbol)
                        api.submit_order(symbol=symbol, qty=position.qty, side='sell', type='market', time_in_force='gtc')
                        self.record_trade(f"SOLD {position.qty} of {symbol}")
                    except Exception as e:
                         if "position not found" not in str(e).lower():
                            print(f"Error selling {symbol}: {e}")

            self.update_portfolio_value()
            time.sleep(60) # Check every minute

    def start(self, investment_amount, risk_level, target_roi, timeframe):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.trading_loop, args=(investment_amount, risk_level, target_roi, timeframe))
        self.thread.start()
        print("Trading bot started.")

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.thread:
            self.thread.join()
        print("Trading bot stopped.")

    def get_status(self):
        with self.lock:
            return {
                "running": self.running,
                "portfolio_value": self.portfolio_value,
                "recent_trades": self.recent_trades
            }

    def record_trade(self, trade):
        with self.lock:
            self.recent_trades.append(trade)

    def update_portfolio_value(self):
        try:
            account_info = api.get_account()
            with self.lock:
                self.portfolio_value = float(account_info.portfolio_value)
        except Exception as e:
            print(f"Error updating portfolio value: {e}")

bot = TradingBot()

# --- API Endpoints ---
@app.route('/start', methods=['POST'])
def start_bot():
    if bot.running:
        return jsonify({"status": "error", "message": "Bot is already running."}), 400
    data = request.json
    bot.start(
        float(data.get('investmentAmount')),
        float(data.get('riskLevel')),
        float(data.get('targetROI')),
        data.get('timeframe')
    )
    return jsonify({"status": "success", "message": "Trading bot started."})

@app.route('/stop', methods=['POST'])
def stop_bot():
    if not bot.running:
        return jsonify({"status": "error", "message": "Bot is not running."}), 400
    bot.stop()
    return jsonify({"status": "success", "message": "Trading bot stopped."})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(bot.get_status())


# --- Backtesting Endpoint ---
@app.route('/backtest', methods=['POST'])
def run_backtest():
    """Runs a backtest for a given symbol and date range."""
    data = request.json
    symbol = data.get('symbol')
    start_date = data.get('startDate')
    end_date = data.get('endDate')

    if not all([symbol, start_date, end_date]):
        return jsonify({"status": "error", "message": "Missing parameters."}), 400

    try:
        backtester = Backtester(start_date=start_date, end_date=end_date)
        results = backtester.run(symbol=symbol)
        return jsonify(results)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001)

from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import os

app = Flask(__name__)

API_KEY = os.environ.get("PKLOI7PEDFZYKOOSN574FAPFJ7")
API_SECRET = os.environ.get("Hc8PJ7YW6jXbu2RewqC5kPJ7iF8fPAS541RxjGsrzKh1")
BASE_URL = os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route('/')
def home():
    return "ORB Webhook Server is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    ticker = data.get("ticker")
    action = data.get("action")  # "buy" or "sell"
    
    if not ticker or not action:
        return jsonify({"error": "Missing ticker or action"}), 400

    try:
        # Close any existing position first
        try:
            api.close_position(ticker)
        except:
            pass

        if action == "buy":
            api.submit_order(
                symbol=ticker,
                notional=8,  # $8 per trade (20% of $40)
                side='buy',
                type='market',
                time_in_force='day'
            )
            return jsonify({"status": "Long order placed", "ticker": ticker}), 200

        elif action == "sell":
            api.submit_order(
                symbol=ticker,
                notional=8,  # $8 per trade
                side='sell',
                type='market',
                time_in_force='day'
            )
            return jsonify({"status": "Short order placed", "ticker": ticker}), 200

        elif action == "close":
            return jsonify({"status": "Position closed", "ticker": ticker}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

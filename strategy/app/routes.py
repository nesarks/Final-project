from flask import Blueprint, render_template, request, abort, current_app
import json
import time
import yfinance as yf
from app.models.user_model import predict_strategy

main = Blueprint('main', __name__)

# Load raw mapping once
with open('data/stock_strategy_mapping.json', 'r') as f:
    raw_map = json.load(f)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        goal    = request.form['goal']
        risk    = request.form['risk']
        horizon = request.form['horizon']

        # 1. Predict the user's strategy
        strategy = predict_strategy(goal, risk, horizon)

        # 2. Build the recommendation list: strip suffix, uppercase, add .NS
        raw_list = raw_map.get(strategy, [])
        recommended_stocks = [
            f"{item.split('_')[0].strip().upper()}.NS"
            for item in raw_list
        ]

        return render_template(
            'result.html',
            strategy=strategy,
            recommended_stocks=recommended_stocks
        )

    return render_template('predict.html')

@main.route('/stock/<ticker>')
def stock_detail(ticker):
    """
    ticker: e.g. 'KOTAKBANK.NS'
    """
    try:
        # Protect against too-fast repeated calls
        time.sleep(0.3)

        yf_symbol = ticker.strip().upper()
        stock = yf.Ticker(yf_symbol)
        hist  = stock.history(period="1y")
        if hist.empty:
            return f"No data found for {yf_symbol}", 404

        info = stock.info
        high = hist['High'].max()
        low  = hist['Low'].min()

        # For display, show the base ticker without suffix
        display_ticker = yf_symbol.split('.')[0]

        return render_template(
            'stock_details.html',
            ticker=display_ticker,
            hist=hist.reset_index().to_dict(orient="records"),
            high=high,
            low=low,
            info=info
        )

    except Exception as e:
        err_str = str(e)
        # Detect common rate-limit messages
        if 'Too Many Requests' in err_str or 'rate limit' in err_str.lower():
            return (
                "Yahoo Finance rate limit reached. "
                "Please wait a minute and refresh.",
                429
            )
        current_app.logger.error(f"Error fetching {ticker}: {e}", exc_info=True)
        abort(500, description=f"Internal error: {e}")

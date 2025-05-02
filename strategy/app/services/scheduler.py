import os
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app.services.stock_metrics import calculate_metrics
from app.services.strategy_assignment import assign_strategy

# Folder with all stock CSVs
STOCK_DATA_FOLDER = "data/stocks"
RESULTS_FILE = "data/assignments/strategy_results.csv"

def process_all_stocks():
    results = []

    for filename in os.listdir(STOCK_DATA_FOLDER):
        if filename.endswith(".csv"):
            stock_name = filename.replace(".csv", "")
            file_path = os.path.join(STOCK_DATA_FOLDER, filename)

            # Read CSV
            column_names = ['Date', 'Price', 'Close', 'High', 'Low', 'Open', 'Volume']
            df = pd.read_csv(file_path, skiprows=2, names=column_names, index_col='Date', parse_dates=['Date'])
            df.index = pd.to_datetime(df.index, errors='coerce')
            df = df.dropna(subset=["Close"])

            # Calculate metrics and assign strategy
            metrics = calculate_metrics(df)
            strategy = assign_strategy(metrics)

            # Store result
            results.append({
                "Stock": stock_name,
                "Volatility": metrics['volatility'],
                "Max Drawdown": metrics['max_drawdown'],
                "MA_30": metrics['ma_30'],
                "MA_180": metrics['ma_180'],
                "MA_365": metrics['ma_365'],
                "Strategy": strategy,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    # Save to CSV
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    pd.DataFrame(results).to_csv(RESULTS_FILE, index=False)
    print(f"[{datetime.now()}] Strategy assignment updated for all stocks.")

def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_all_stocks, trigger="cron", hour=6, minute=0)  # Run daily at 6:00 AM
    scheduler.start()
    print("Scheduler initialized. Daily update job added.")

# generate_strategy_mapping.py

import os
import json
import pandas as pd
from app.services.stock_metrics import calculate_metrics
from app.services.strategy_assignment import assign_strategy

stock_folder = "data/stocks"
output_path = "data/stock_strategy_mapping.json"
column_names = ['Date', 'Price', 'Close', 'High', 'Low', 'Open', 'Volume']

strategy_map = {}

for file in os.listdir(stock_folder):
    if file.endswith(".csv"):
        stock_name = file.replace(".csv", "")
        try:
            df = pd.read_csv(os.path.join(stock_folder, file), skiprows=2, names=column_names, parse_dates=['Date'])
            df.dropna(subset=["Close"], inplace=True)
            metrics = calculate_metrics(df)
            strategy = assign_strategy(metrics)
            strategy_map.setdefault(strategy, []).append(stock_name)
            print(f"✅ {stock_name} → {strategy}")
        except Exception as e:
            print(f"❌ Error processing {stock_name}: {e}")

# Save to JSON
with open(output_path, "w") as f:
    json.dump(strategy_map, f, indent=2)

print(f"\n📁 Strategy mapping saved to: {output_path}")

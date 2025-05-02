import pandas as pd
from app.services.stock_metrics import calculate_metrics
from app.services.strategy_assignment import assign_strategy

# Manually set the column names
column_names = ['Date', 'Price', 'Close', 'High', 'Low', 'Open', 'Volume']

# Load the CSV, skipping the first row
stock_data = pd.read_csv("data/stocks/RELIANCE_nifty50.csv", skiprows=2, names=column_names, index_col='Date', parse_dates=['Date'])

# Convert the index to datetime format
stock_data.index = pd.to_datetime(stock_data.index, errors='coerce')

# Drop rows with NaT in the index (if any)
stock_data = stock_data.dropna(subset=["Close"])  # Ensuring no NaNs in critical column

# Display the first few rows to verify the data
print("Sample stock data:\n", stock_data.head())

# Calculate the metrics using the loaded stock data
metrics = calculate_metrics(stock_data)

# Print the calculated metrics
print("\nCalculated Metrics for RELIANCE:")
print(metrics)

# Assign investment strategy based on metrics
strategy = assign_strategy(metrics)

# Print the assigned strategy
print("\nAssigned Strategy for RELIANCE:", strategy)

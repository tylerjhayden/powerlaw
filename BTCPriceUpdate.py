import yfinance as yf
import pandas as pd
import os

# Define the CSV file path
csv_file = 'btc_price_data.csv'

def fetch_full_data():
    """Fetch and save the full historical Bitcoin data."""
    btc_data = yf.Ticker("BTC-USD")
    hist = btc_data.history(period="max")
    hist.to_csv(csv_file)
    print(f"Full historical Bitcoin price data has been saved to '{csv_file}'")

def update_data():
    """Update the existing CSV with the latest Bitcoin data."""
    # Read existing data
    existing_data = pd.read_csv(csv_file, index_col='Date', parse_dates=True)
    
    # Get the last date from the existing data
    last_date = existing_data.index[-1]
    
    # Fetch new data from the last date up to today
    btc_data = yf.Ticker("BTC-USD")
    new_data = btc_data.history(start=last_date)
    
    # Remove the overlapping last date to avoid duplication
    new_data = new_data.loc[new_data.index > last_date]
    
    if not new_data.empty:
        # Append new data to existing data
        updated_data = existing_data.append(new_data)
        
        # Save the updated data back to the CSV
        updated_data.to_csv(csv_file)
        print(f"Bitcoin price data has been updated in '{csv_file}'")
    else:
        print("No new data to update.")

# Main logic
if os.path.exists(csv_file):
    update_data()
else:
    fetch_full_data()

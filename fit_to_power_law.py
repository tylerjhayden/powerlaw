import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# Load the Bitcoin price data
print("Loading the price data from csv")
data = pd.read_csv('btc_price_data.csv', parse_dates=['Date'], index_col='Date')

# Ensure the data is sorted by date
data.sort_index(inplace=True)

# Convert dates to numerical values (days since the first date)
data['Days'] = (data.index - data.index[0]).days

# Remove any zero or negative prices (cannot take log of zero or negative numbers)
data = data[data['Close'] > 0]

# Prepare x and y for fitting
print("Preparing x and y for fitting")
x = data['Days'].values
y = data['Close'].values

# Take logarithms
log_x = np.log(x + 1)  # Add 1 to avoid log(0)
log_y = np.log(y)

# Fit the linear model to log-log data
print("running polyfit on log_x & log_y to find coefficients...")
print("np.polyfit fits a line to the log-log data.")
coefficients = np.polyfit(log_x, log_y, 1)
b = coefficients[0]
log_a = coefficients[1]
a = np.exp(log_a)

# Print the model parameters
print(f"Model parameters:")
print(f"a = {a}")
print(f"b = {b}")

# Create the model data
data['Model'] = a * (x + 1) ** b  # Add 1 to x to match the transformation

# Save the model data to a CSV file
model_csv_file = 'btc_power_law_model.csv'
data[['Model']].to_csv(model_csv_file)
print(f"Power law model data has been saved to '{model_csv_file}'")

# Plot the model
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Actual BTC Price')
plt.plot(data.index, data['Model'], label='Power Law Model', linestyle='--')
plt.title('Bitcoin Price and Power Law Model Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()
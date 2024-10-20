import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the Bitcoin price data
data = pd.read_csv('btc_price_data.csv', parse_dates=['Date'], index_col='Date')
data.sort_index(inplace=True)

# Load the model data
model_data = pd.read_csv('btc_power_law_model.csv', parse_dates=['Date'], index_col='Date')
model_data.sort_index(inplace=True)

# Ensure both dataframes are aligned
data = data.join(model_data, how='inner')

# Convert dates to numerical values (days since the first date)
data['Days'] = (data.index - data.index[0]).days + 1  # Add 1 to avoid zero

# Prepare data for plotting
x = data['Days'].values
y_actual = data['Close'].values
y_model = data['Model'].values

# Remove any zero or negative values before taking logs
mask = (x > 0) & (y_actual > 0) & (y_model > 0)
x = x[mask]
y_actual = y_actual[mask]
y_model = y_model[mask]

# Plot on a log-log scale
plt.figure(figsize=(12, 6))
plt.loglog(x, y_actual, label='Actual BTC Price')
plt.loglog(x, y_model, label='Power Law Model', linestyle='--')
plt.title('Bitcoin Price and Power Law Model on Log-Log Scale')
plt.xlabel('Days Since First Data Point')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Load the Bitcoin price data
data = pd.read_csv('btc_price_data.csv', parse_dates=['Date'], index_col='Date')
data.sort_index(inplace=True)

# Load the model data (which now includes the projection)
model_data = pd.read_csv('btc_power_law_model.csv', parse_dates=['Date'], index_col='Date')
model_data.sort_index(inplace=True)

# Convert dates to numerical values (days since the first date)
start_date = data.index[0]
data['Days'] = (data.index - start_date).days + 1  # Add 1 to avoid zero
model_data['Days'] = (model_data.index - start_date).days + 1

# Prepare data for plotting
x_actual = data['Days'].values
y_actual = data['Close'].values

x_model = model_data['Days'].values
y_model = model_data['Model'].values

# Remove any zero or negative values before taking logs
mask_actual = (x_actual > 0) & (y_actual > 0)
x_actual = x_actual[mask_actual]
y_actual = y_actual[mask_actual]

mask_model = (x_model > 0) & (y_model > 0)
x_model = x_model[mask_model]
y_model = y_model[mask_model]

# Plot on a log-log scale
plt.figure(figsize=(12, 6))
plt.loglog(x_actual, y_actual, label='Actual BTC Price')
plt.loglog(x_model, y_model, label='Power Law Model (Projected)', linestyle='--')
plt.title('Bitcoin Price and Power Law Model on Log-Log Scale (with Projection)')
plt.xlabel('Days Since First Data Point')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True, which="both", ls="--")

# Customize the y-axis ticks
ax = plt.gca()
ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))

# Optionally, customize the x-axis ticks if needed
# ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
# ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))

plt.show()
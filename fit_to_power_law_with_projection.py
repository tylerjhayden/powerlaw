import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.ticker as ticker


# how many days would you like to project forward?
projection_years = 10
print(f"Years forward the model will project: {projection_years}")

# Load the Bitcoin price data
data = pd.read_csv('btc_price_data.csv', parse_dates=['Date'], index_col='Date')

# Ensure the data is sorted by date
data.sort_index(inplace=True)

# Convert dates to numerical values (days since the first date)
data['Days'] = (data.index - data.index[0]).days

# Remove any zero or negative prices (cannot take log of zero or negative numbers)
data = data[data['Close'] > 0]

# Prepare x and y for fitting
x = data['Days'].values
y = data['Close'].values

# Take logarithms
log_x = np.log(x + 1)  # Add 1 to avoid log(0)
log_y = np.log(y)

# Fit the linear model to log-log data
coefficients = np.polyfit(log_x, log_y, 1)
b = coefficients[0]
log_a = coefficients[1]
a = np.exp(log_a)

# Print the model parameters
print(f"Model parameters:")
print(f"a = {a}")
print(f"b = {b}")

# Create the model data for the existing dates
data['Model'] = a * (x + 1) ** b  # Add 1 to x to match the transformation

# Project the model forward 10 years

# Calculate the last date in the original data
last_date = data.index[-1]

# Create a date range extending projection_years beyond the last date
projection_days = projection_years * 365  # Approximate number of days
extended_dates = pd.date_range(start=last_date + timedelta(days=1), periods=projection_days, freq='D')

# Create a DataFrame for the extended dates
extended_data = pd.DataFrame(index=extended_dates)

# Calculate 'Days' for the extended data (days since the first date)
extended_data['Days'] = (extended_data.index - data.index[0]).days

# Calculate the model prices for the extended dates
x_extended = extended_data['Days'].values
extended_data['Model'] = a * (x_extended + 1) ** b  # Add 1 to x to match the transformation

# Combine the original and extended model data
full_model_data = pd.concat([data[['Model']], extended_data[['Model']]], axis=0)

# Name the index as 'Date'
full_model_data.index.name = 'Date'

# Save the full model data to a CSV file
model_csv_file = 'btc_power_law_model.csv'
full_model_data.to_csv(model_csv_file)
print(f"Power law model data (including a projection) has been saved to '{model_csv_file}'")

# Plot the actual data and the extended model
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Actual BTC Price')
plt.plot(full_model_data.index, full_model_data['Model'], label='Power Law Model (Projected)', linestyle='--')
plt.title('Bitcoin Price and Power Law Model Over Time (with Projection)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)


# # Get the current axes
# ax = plt.gca()

# # Customize the y-axis major ticks
# ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
# ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))

# # Customize the y-axis minor ticks
# ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(1.0, 10.0), numticks=100))
# ax.yaxis.set_minor_formatter(ticker.NullFormatter())  # Hide minor tick labels

# # Enable minor grid lines
# ax.grid(True, which='minor', linestyle=':', linewidth=0.5)

plt.show()



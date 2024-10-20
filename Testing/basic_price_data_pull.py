import yfinance as yf
import matplotlib.pyplot as plt

# Fetch historical Bitcoin data using yfinance. Create a ticker object. 
btc_data = yf.Ticker("BTC-USD")

# data is returned in Pandas DataFrame format

# Download the historical data (last 6 months)
hist = btc_data.history(period="5y") #"5y" is 5 years
info = btc_data.info
print(info)

# Plot the closing prices
plt.figure(figsize=(10, 6))
plt.plot(hist.index, hist['Close'], label='BTC-USD Close Price')
plt.title('Bitcoin Price Over the Last 5 years')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.legend()

# Display the plot
plt.show()
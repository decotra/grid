import pandas as pd
import matplotlib.pyplot as plt

# Example Dogecoin price series
date_rng = pd.date_range(start="2023-10-01", end="2023-10-30", freq="D")
dogecoin_prices = pd.Series([0.28, 0.32, 0.31, 0.29, 0.30, 0.33, 0.34, 0.35, 0.36, 0.38, 0.39, 0.40, 0.42, 0.41, 0.43, 0.45, 0.46, 0.47, 0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59], index=date_rng)

# Example list of trades
trades = [
    {'date': "2023-10-05", 'price': 0.32},
    {'date': "2023-10-15", 'price': 0.43},
    {'date': "2023-10-25", 'price': 0.55}
]

# Convert trade dates to datetime objects
trade_dates = pd.to_datetime([trade['date'] for trade in trades])

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(dogecoin_prices.index, dogecoin_prices.values, label='Dogecoin Price', color='b')
plt.scatter(trade_dates, [trade['price'] for trade in trades], color='r', label='Trade', marker='o', s=100)

# Customize the plot
plt.title('Dogecoin Price with Trade Markers')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
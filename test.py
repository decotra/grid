#%%
import binance_ohlcv as bo
from datetime import date


df = bo.get_spot(symbol="DOGEUSDT", start=date(2023, 10, 1), end=date(2023, 10, 1), timeframe='1s')

prices = df['close']

for index, price in prices.items():
    print(index, price)
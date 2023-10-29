# %%
import binance_ohlcv as bo
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Trade:
    def __init__(self, timestamp, price):
        self.timestamp = timestamp
        self.price = price


class Buy(Trade):
    def __init__(self, timestamp, price):
        super().__init__(timestamp, price)


class Sell(Trade):
    def __init__(self, timestamp, price):
        super().__init__(timestamp, price)


class TradeList(list):
    def timestamps(self):
        return [trade.timestamp for trade in self]

    def prices(self):
        return [trade.price for trade in self]


class Backtest:
    def __init__(self, start_usdt, start, end, symbol, step, order_usdt, comm_rate):
        self.start_usdt = start_usdt

        self.start = start
        self.end = end
        self.symbol = symbol
        self.step = step
        self.order_usdt = order_usdt
        self.comm_rate = comm_rate
        self.order_comm = self.order_usdt * self.comm_rate

        logger.debug(
            f"{self.start=}, {self.end=}, {self.symbol=}, {self.step=}, {self.order_usdt=}"
        )
        logger.debug(f"{self.comm_rate=}, {self.order_comm=}")

        # variables
        self.usdt = 0
        self.coin = 0
        self.total_comm = 0

        self.buy_trades = TradeList()
        self.sell_trades = TradeList()

    def run(self):
        self.prices = self.load_prices()
        self.start_price = self.prices.iloc[0]
        self.end_price = self.prices.iloc[-1]

        self.usdt = self.start_usdt / 2
        self.coin = self.start_usdt / 2 / self.start_price

        self.mid = self.start_price
        self.buy_price = self.mid * (1 - self.step)
        self.sell_price = self.mid * (1 + self.step)

        logger.debug(
            f"{self.usdt=}, {self.coin=}, {self.mid=}, {self.buy_price=}, {self.sell_price=}"
        )

        for timestamp, price in self.prices.items():
            self.timestamp = timestamp
            if price < self.buy_price and self.usdt > 0:
                self.buy()
                self.mid = self.buy_price
                self.buy_price = self.mid * (1 - self.step)
                self.sell_price = self.mid * (1 + self.step)
            elif price > self.sell_price and self.coin > 0:
                self.sell()
                self.mid = self.sell_price
                self.buy_price = self.mid * (1 - self.step)
                self.sell_price = self.mid * (1 + self.step)

        self.end_value_usdt = self.end_price * self.coin + self.usdt

        summary = f"{self.start_price=}, {self.end_price=}, {self.start_usdt=}, {self.end_value_usdt=}"

        logger.info(summary)

    def buy(self):
        order_coin = self.order_usdt / self.buy_price
        self.adjust_comm()
        self.coin += order_coin
        self.usdt -= self.order_usdt

        self.buy_trades.append(Buy(self.timestamp, self.buy_price))
        self.log_buy()

    def sell(self):
        order_coin = self.order_usdt / self.sell_price
        self.adjust_comm()
        self.coin -= order_coin
        self.usdt += self.order_usdt

        self.sell_trades.append(Sell(self.timestamp, self.sell_price))
        self.log_sell()

    def log_buy(self):
        self.log_trade('BUY ')

    def log_sell(self):
        self.log_trade('SELL')

    def log_trade(self, side):
        logger.debug(
            f"{self.timestamp} {side} price: {self.sell_price:.4f} usdt: {self.usdt:.2f} coin: {self.coin:.2f}"
            f"total_comm: {self.total_comm:.2f} current_value: {self.current_value:.2f}"
        )

    def adjust_comm(self):
        self.total_comm += self.order_comm
        self.usdt -= self.order_comm

    @property
    def current_value(self):
        return self.prices[self.timestamp] * self.coin + self.usdt

    def load_prices(self):
        df = bo.get_spot(
            symbol=self.symbol, start=self.start, end=self.end, timeframe="1s"
        )
        return df["close"]

    def plot(self):
        # Create the plot
        plt.figure(figsize=(10, 5))
        plt.plot(self.prices.index, self.prices.values, label='price', color='b')
        plt.scatter(self.buy_trades.timestamps(), self.buy_trades.prices(), color='r', label='buy', marker='^', s=100)
        plt.scatter(self.sell_trades.timestamps(), self.sell_trades.prices(), color='g', label='sell', marker='v',
                    s=100)

        # Customize the plot
        plt.title('Price with Trade Markers')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()

        # Show the plot
        plt.grid(True)
        plt.show()


start = date(2023, 1, 1)
end = date(2023, 10, 28)
symbol = "DOGEUSDT"
step = 0.01
order_usdt = 300
comm_rate = 0.001
start_usdt = 10000

bt = Backtest(
    symbol=symbol,
    start=start,
    end=end,
    step=step,
    order_usdt=order_usdt,
    comm_rate=comm_rate,
    start_usdt=start_usdt,
)
bt.run()

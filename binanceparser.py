import json

from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from config import *


class Trade:

    def __init__(self, start_base: str, start_quote: str, start_count: int):
        self._client = Client(API_KEY, SECRET_KEY)
        self._start_base = start_base
        self._start_quote = start_quote
        self._start_symbol = self._start_base + self._start_quote
        self._last_symbol = self._start_symbol
        self._last_trade = {}
        self._trades = []
        self._circles = []
        self._start_count = start_count
        self._count = self._start_count
        self._base = self._start_base
        self._quote = self._start_quote
        self._data = self.get_data()
        self._bundles = self.find_bundles()

    @staticmethod
    def get_bids(death):
        return death["bids"]

    @staticmethod
    def get_asks(death):
        return death["asks"]

    @staticmethod
    def get_data():
        with open("symbols.json") as f: return json.load(f)["data"]

    def get_death(self, symbol="BTCUSDT"):
        try:
            return self._client.get_order_book(symbol=symbol)
        except Exception as e:
            print(e, symbol)
            return None

    def buy(self):
        trade = {
            "base": self._base,
            "quote": self._quote,
            "before_count": self._count,
            "after_count": 0,
            "ask": 0,
        }
        self._last_symbol = self._quote + self._base
        death = self.get_death(self._last_symbol)
        asks = self.get_asks(death)
        self._count = self._count / float(asks[0][0])
        trade["after_count"] = self._count
        trade["ask"] = asks[0][0]
        self._base = self._quote
        self._last_trade = trade
        self._trades.append(trade)

    def sell(self, quote):
        self._quote = quote
        trade = {
            "base": self._base,
            "quote": self._quote,
            "before_count": self._count,
            "after_count": 0,
            "bid": 0,
        }
        self._last_symbol = self._quote + self._base
        death = self.get_death(self._last_symbol)
        bids = self.get_bids(death)
        self._count = self._count / float(bids[0][0])
        trade["after_count"] = self._count
        trade["ask"] = bids[0][0]
        self._last_trade = trade
        self._trades.append(trade)
        self._base = self._quote

    def end_circle(self):
        trade = {
            "base": self._base,
            "quote": self._start_base,
            "before_count": self._count,
            "after_count": 0,
            "bid": 0,
        }
        self._last_symbol = self._base + self._start_base
        death = self.get_death(self._last_symbol)
        bids = self.get_bids(death)
        self._count = self._count * float(bids[0][0])
        trade["after_count"] = self._count
        trade["ask"] = bids[0][0]
        self._last_trade = trade
        self._trades.append(trade)
        circle = {}
        for i, t in enumerate(self._trades, start=1):
            circle[f"{i}"] = str(t["quote"] + t["base"])
        circle["spred"] = self.get_spred()
        circle["spred_p"] = self.get_spred_percent()
        self._circles.append(circle)

    def get_spred(self):
        return self._count - self._start_count

    def get_spred_percent(self):
        percentage = 100 * float(self._count - self._start_count) / float(self._start_count)
        return percentage

    def get_last_trade(self):
        return self._last_trade

    def get_all_trades(self):
        return self._trades

    def find_bundles(self) -> list:
        array = []
        for d in self._data:
            if d["quote"] == self._quote:
                array.append([d["base"], d["quote"]])
        return array

    def get_bundles(self):
        return self._bundles

    def reset(self):
        self._start_symbol = self._start_base + self._start_quote
        self._last_symbol = self._start_symbol
        self._count = self._start_count
        self._base = self._start_base
        self._quote = self._start_quote
        self._trades = []

    def get_circles(self):
        return self._circles


if __name__ == '__main__':
    trade = Trade("USDT", "BTC", 1000)
    trade.buy()
    trade.sell("XRP")
    trade.end_circle()
    print(trade.get_all_trades())
    print(trade.get_spred())
    print(trade.get_spred_percent())

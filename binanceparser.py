from binance import Client
from config import *


class TriangularArbitration:
    def __init__(self, start_quote: str, start_count: int = 1000):
        self._client = Client(API_KEY, SECRET_KEY)
        self._start_quote = start_quote
        self._comission = 0.1
        self._start_count = start_count
        self._symbols = self.get_symbols()
        self._connexions = self.get_connexions(self._start_quote)
        self._all_connexions = [con["symbol"] for con in self._symbols]
        self._prices = self.get_prices()

    def base_to_quote(self, base_value, bid) -> float:
        base_value = float(base_value)
        bid = float(bid)
        full_comission = base_value / 100 * self._comission
        return bid * (base_value - full_comission)

    def quote_to_base(self, quote_value, ask) -> float:
        quote_value = float(quote_value)
        ask = float(ask)
        full_comission = quote_value / 100 * self._comission
        return (quote_value - full_comission) / ask

    def get_symbols(self) -> list:
        return self._client.get_exchange_info()["symbols"]

    def get_prices(self) -> dict:
        return self._client.get_orderbook_tickers()

    def get_connexions(self, quote) -> list:
        array = []
        for symbol in self._symbols:
            if symbol["quoteAsset"] == quote:
                array.append(symbol["baseAsset"] + "/" + symbol["quoteAsset"])
        return array

    def find_orderbook_ticker(self, symbols: list):
        array = []
        for price in self._prices:
            if price["symbol"] in symbols:
                array.append(price)
        return array

    def get_circles(self):
        circles = []
        for con in self._connexions:
            base, quote = con.split("/")
            for con2 in self.get_connexions(base):
                base2, quote2 = con2.split("/")
                if base2 + self._start_quote not in self._all_connexions: continue
                symbols = [base + quote, base2 + quote2, base2 + self._start_quote]
                circle = self.find_orderbook_ticker(symbols)
                circles.append(circle)
        return circles

    def normalize_circle(self, circle):
        array = [0.0] * 3
        for symbol in circle:
            bid = float(symbol["bidPrice"])
            ask = float(symbol["askPrice"])
            if bid == 0 or ask == 0: return None
            if symbol["symbol"].endswith(self._start_quote):
                if array[0] == 0:
                    array[0] = symbol
                else:
                    array[2] = symbol
            else:
                array[1] = symbol

        return array

    def find_spreads(self):
        self._prices = self.get_prices()
        trades = []
        circles = self.get_circles()
        for circle in circles:
            c = self.normalize_circle(circle)
            count = self._start_count
            base1 = ""
            if c is None: continue
            if len(c) == 3:
                for i, symbol in enumerate(c):
                    bid = float(symbol["bidPrice"])
                    ask = float(symbol["askPrice"])
                    if i == 0:
                        base1 = symbol["symbol"].replace(self._start_quote, "")
                        count = self.quote_to_base(count, ask)
                    elif i == 1:
                        if symbol["symbol"].startswith(base1):
                            count = self.base_to_quote(count, bid)
                        else:
                            count = self.quote_to_base(count, ask)
                    elif i == 2:
                        count = self.base_to_quote(count, bid)
            spred = 100 * float(count - self._start_count) / float(self._start_count)
            c.append(spred)
            trades.append(c)
        return trades

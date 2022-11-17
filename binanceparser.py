from binance import Client
import config
import requests
import threading


class TriangularArbitration:
    def __init__(self, start_quote: str, start_count: int = 100000):
        self._client = Client(config.API_KEY, config.SECRET_KEY)
        self._start_quote = start_quote
        self._comission = 0.1
        self._start_count = start_count
        self._symbols = self._get_symbols()
        self.connexions = self._get_connexions(self._start_quote)
        self._all_connexions = [con["symbol"] for con in self._symbols]
        self._prices = self._get_prices()
        self._res = []
        self._session = requests.Session()

    def _get(self, data):
        self._res.append(self._session.post(config.URL_P2P, headers=config.headers, json=data).json())

    def _base_to_quote(self, base_value, bid) -> float:
        base_value = float(base_value)
        bid = float(bid)
        full_comission = base_value / 100 * self._comission
        return bid * (base_value - full_comission)

    def _quote_to_base(self, quote_value, ask) -> float:
        quote_value = float(quote_value)
        ask = float(ask)
        full_comission = quote_value / 100 * self._comission
        return (quote_value - full_comission) / ask

    def _get_symbols(self) -> list:
        return self._client.get_exchange_info()["symbols"]

    def _get_prices(self) -> dict:
        return self._client.get_orderbook_tickers()

    def _get_connexions(self, quote) -> list:
        array = []
        for symbol in self._symbols:
            if symbol["quoteAsset"] == quote:
                array.append(symbol["baseAsset"] + "/" + symbol["quoteAsset"])
        return array

    def _find_orderbook_ticker(self, symbols: list):
        array = []
        for price in self._prices:
            if price["symbol"] in symbols:
                array.append(price)
        return array

    def get_circles(self):
        circles = []
        for con in self.connexions:
            base, quote = con.split("/")
            for con2 in self._get_connexions(base):
                base2, quote2 = con2.split("/")
                if base2 + self._start_quote not in self._all_connexions: continue
                symbols = [base + quote, base2 + quote2, base2 + self._start_quote]
                circle = self._find_orderbook_ticker(symbols)
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

    def find_p2p(self):
        advs = []
        json_data = []
        self._res = []
        for asset in config.ASSETS:
            for bank in config.BANKS:
                data = config.data_buy.copy()
                data["payTypes"] = [bank]
                data["asset"] = asset
                json_data.append(data)
        th = []
        for data in json_data:
            t = threading.Thread(target=self._get, args=(data,))
            t.start()
            th.append(t)
        for t in th:
            t.join()
        for r in self._res:
            r_data = r["data"]
            if len(r_data) == 0: continue
            adv = r_data[0]
            advs.append(adv)
        advs = sorted(advs, key=lambda x: x["adv"]["price"])
        offers = []
        for i, advertisers1 in enumerate(advs):
            price1 = float(advertisers1["adv"]["price"])
            ass = advertisers1["adv"]["asset"]
            max_single_trans_amount = float(advertisers1["adv"]["maxSingleTransAmount"])
            min_single_trans_amount = float(advertisers1["adv"]["minSingleTransAmount"])
            advertiserNo1 = advertisers1["advertiser"]["userNo"]
            if min_single_trans_amount <= self._start_count <= max_single_trans_amount:
                banks1 = [x["tradeMethodName"] for x in advertisers1["adv"]["tradeMethods"]]
                for asset2 in range(i + 1, len(advs)):
                    advertisers2 = advs[asset2]["adv"]
                    advertiserNo2 = advs[asset2]["advertiser"]["userNo"]
                    ass2 = advertisers2["asset"]
                    if ass2 == ass:
                        banks2 = [x["tradeMethodName"] for x in advertisers2["tradeMethods"]]
                        if all(x not in banks1 for x in banks2):
                            price2 = float(advertisers2["price"])
                            count_buy = self._start_count / price1
                            count_sell = (count_buy * price2) - (count_buy * config.COMISSION_P2P)
                            spred = 100 * float(count_sell - self._start_count) / float(self._start_count)
                            offer = {
                                "BUY": {
                                    "asset": ass,
                                    "price": price1,
                                    "banks": banks1,
                                    "balance": count_buy,
                                    "advertiserNo": advertiserNo1
                                },
                                "SELL": {
                                    "asset": ass2,
                                    "price": price2,
                                    "banks": banks2,
                                    "balance": count_sell,
                                    "advertiserNo": advertiserNo2
                                },
                                "SPRED": spred
                            }
                            if offer not in offers:
                                offers.append(offer)
        offers = sorted(offers, key=lambda d: d["SPRED"], reverse=True)
        return offers

    def find_spreads(self):
        self._prices = self._get_prices()
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
                        count = self._quote_to_base(count, ask)
                    elif i == 1:
                        if symbol["symbol"].startswith(base1):
                            count = self._base_to_quote(count, bid)
                        else:
                            count = self._quote_to_base(count, ask)
                    elif i == 2:
                        count = self._base_to_quote(count, bid)
            spred = 100 * float(count - self._start_count) / float(self._start_count)
            c.append(spred)
            trades.append(c)
        return sorted(trades, key=lambda d: d[-1], reverse=True)

import json

API_KEY = "tWoRZ5wUN0JDoMyzpc4FGm0KI2Aex5vnI55upSsaZGtSZ7W2mZ7OrX2enleeSvIY"
SECRET_KEY = "JyY0N1H3g8B05M0zYxve5Om56OBvICZMAUVCoeBrmvkyyqpohD58IKGm6s6RjsTh"
BOT_TOKEN = "5647535683:AAGFPSi6mEhAcT0DlKjgfzomHJthtAGV4AQ"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "123",
    "content-type": "application/json",
    "Host": "p2p.binance.com",
    "Origin": "https://p2p.binance.com",
    "Pragma": "no-cache",
    "TE": "Trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

data_buy = {
    "asset": "USDT",
    "fiat": "RUB",
    "merchantCheck": False,
    "page": 1,
    "payTypes": ["RosBankNew"],
    "publisherType": None,
    "rows": 20,
    "tradeType": "BUY"
}

BANKS = ["YandexMoneyNew", "RosBankNew", "HomeCreditBank", "RaiffeisenBank", "TinkoffNew", "RosBankNew", "MTSBank",
         "UralsibBank",
         "QIWI"]

ASSETS = ["BTC", "USDT", "BNB", "BUSD"]

FIAT = "RUB"

COMISSION_P2P = 0.1

URL_P2P = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

URL_USER = "https://p2p.binance.com/ru/advertiserDetail?advertiserNo="

with open("messages.json", encoding="utf-8") as f: MESSAGES = json.load(f)
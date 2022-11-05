from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

ustd = InlineKeyboardButton("USDT", callback_data='select_ustd'),
btc = InlineKeyboardButton("BTC", callback_data='select_btc'),
eth = InlineKeyboardButton("ETH", callback_data='select_eth'),
shib = InlineKeyboardButton("SHIB", callback_data='select_shib'),
bnb = InlineKeyboardButton("BNB", callback_data='select_bnb')
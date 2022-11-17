from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

ustd = InlineKeyboardButton("USDT", callback_data='select_ustd')
btc = InlineKeyboardButton("BTC", callback_data='select_btc')
eth = InlineKeyboardButton("ETH", callback_data='select_eth')
shib = InlineKeyboardButton("SHIB", callback_data='select_shib')
bnb = InlineKeyboardButton("BNB", callback_data='select_bnb')
show_bundles = InlineKeyboardButton("Показать связки", callback_data='show_bundles')
how_it_works = InlineKeyboardButton("Как это работает?", callback_data='how_it_works')
show_more = InlineKeyboardButton("Показать еще", callback_data='show_more')
select_asset = InlineKeyboardButton("Выбрать актив", callback_data='select_asset')
back = InlineKeyboardButton("Назад", callback_data='back')

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

ustd = InlineKeyboardButton("USDT", callback_data='select_usdt')
bustd = InlineKeyboardButton("BUSD", callback_data='select_busd')
btc = InlineKeyboardButton("BTC", callback_data='select_btc')
eth = InlineKeyboardButton("ETH", callback_data='select_eth')
bnb = InlineKeyboardButton("BNB", callback_data='select_bnb')
show_bundles = InlineKeyboardButton("Показать связки", callback_data='show_bundles')
show_bundles_p2p = InlineKeyboardButton("Показать связки P2P", callback_data='show_bundles_p2p')
how_it_works = InlineKeyboardButton("Как это работает?", callback_data='how_it_works')
show_more = InlineKeyboardButton("Показать еще", callback_data='show_more')
select_asset = InlineKeyboardButton("Выбрать актив", callback_data='select_asset')
back = InlineKeyboardButton("Назад", callback_data='back')

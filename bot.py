import time

import telebot

import config
import markups
from BinanceParser import *

bot = telebot.TeleBot(config.BOT_TOKEN)
user_dict = {}


class User:
    def __init__(self):
        self.asset = None
        self.order = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    mk = telebot.types.InlineKeyboardMarkup(row_width=2)
    mk.add(markups.show_bundles, markups.how_it_works)
    bot.send_message(
        message.chat.id, config.MESSAGES["start_message"], reply_markup=mk)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    bot.send_message(message.chat.id, config.MESSAGES["help_message"])


@bot.message_handler(commands=['how_it_works'])
def send_help(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    bot.send_message(message.chat.id, config.MESSAGES["how_it_works_message"])


@bot.message_handler(commands=['search_spreads'])
def search_spreads(message):
    show_bundles(message)


@bot.message_handler(commands=['search_spreads_p2p'])
def search_spreads_p2p(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    start_time = time.time()
    bot.send_message(
        message.chat.id, config.MESSAGES["search_spred_p2p_message"], )
    trade = TriangularArbitration("USDT")
    circles = trade.find_p2p()
    for circle in circles[:5]:
        print(circle)
        buy = circle["BUY"]
        sell = circle["SELL"]

        buy_asset = buy["asset"]
        buy_price = buy["price"]
        buy_banks = " ИЛИ ".join(buy["banks"])

        sell_price = sell["price"]
        sell_banks = " ИЛИ ".join(sell["banks"])

        spred = str(round(circle["SPRED"], 2)) + "%"
        userNo = config.URL_USER + buy["advertiserNo"]
        text = config.MESSAGES["spred_p2p_message"].format(buy_banks, buy_asset, buy_price, sell_banks,
                                                           sell_price, spred, userNo)
        bot.send_message(message.chat.id, text,
                         parse_mode="Markdown", disable_web_page_preview=True)
    #bot.delete_message(message.chat.id, message.id + 1)

    bot.send_message(message.chat.id, "--- %s seconds ---" %
                     (time.time() - start_time))


@bot.callback_query_handler(lambda query: query.data == 'show_bundles')
def show_bundles(query):
    try:
        message = query.message
    except:
        message = query
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    text = config.MESSAGES["select_asset_message"]
    try:
        mk = telebot.types.InlineKeyboardMarkup()
        mk.add(markups.bnb, markups.btc, markups.eth,
               markups.ustd, markups.bustd, markups.back)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,
                              reply_markup=mk)
    except:
        mk = telebot.types.InlineKeyboardMarkup()
        mk.add(markups.bnb, markups.btc, markups.eth,
               markups.ustd, markups.bustd)
        bot.send_message(message.chat.id, text, reply_markup=mk)


@bot.callback_query_handler(lambda query: query.data == 'back')
def back(query):
    bot.clear_step_handler_by_chat_id(chat_id=query.message.chat.id)
    bot.delete_message(query.message.chat.id, query.message.message_id)
    send_welcome(query.message)


@bot.callback_query_handler(lambda query: query.data == 'how_it_works')
def how_it_works(query):
    mk = telebot.types.InlineKeyboardMarkup()
    mk.add(markups.back)
    text = config.MESSAGES["how_it_works_message"]
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                          text=text, reply_markup=mk)


@bot.callback_query_handler(lambda query: query.data.startswith('select_'))
def ans(query):
    chat_id = query.message.chat.id
    user = User()
    user_dict[chat_id] = user
    user = user_dict[chat_id]
    user_asset = query.data.split("_")[1]
    user.order = query.message.text
    user.asset = user_asset
    mk = telebot.types.InlineKeyboardMarkup()
    mk.add(markups.back)
    msg = bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=config.MESSAGES["enter_order_amount_message"], reply_markup=mk)
    bot.register_next_step_handler(msg, process_order_step)


def process_order_step(message):
    chat_id = message.chat.id
    order = message.text.replace(",", ".")
    user = user_dict[chat_id]
    try:
        user.order = float(order)
    except:
        msg = bot.reply_to(
        message, 'Сумма ордера должна быть числом. Попробуйте еще раз!')
        bot.register_next_step_handler(msg, process_order_step)
        return
    start_time = time.time()
    bot.send_message(
        message.chat.id, config.MESSAGES["search_spreads_message"])
    trade = TriangularArbitration(user.asset.upper(), start_count=user.order)
    circles = trade.find_spreads()
    for circle in circles[:5]:
        print(circle)
        bot.send_message(message.chat.id,
                         "*Спред: {0}\n{1} - {2}\n{3} - {4}\n{5} - {6}*".format(f"{circle[-1]:.2f}%", circle[0]["symbol"],
                                                                                circle[0]["askPrice"],
                                                                                circle[1]["symbol"],
                                                                                circle[1]["askPrice"],
                                                                                (circle[2])[
                             "symbol"],
                             circle[0]["bidPrice"]),
                         parse_mode="Markdown")
    # bot.delete_message(message.chat.id, message.id + 1)
    bot.send_message(message.chat.id, "--- %s seconds ---" %
                     (time.time() - start_time))
    mk = telebot.types.InlineKeyboardMarkup()
    mk.add(markups.show_bundles)
    bot.send_message(
        message.chat.id, "Из нас получилась отличная команда! Продолжим в том же духе?", reply_markup=mk)


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()

import json
import time
from config import *
import telebot
from binanceparser import *

bot = telebot.TeleBot(BOT_TOKEN)

with open("messages.json", encoding="utf-8") as f: messages = json.load(f)


def circles_sort(circle: list) -> list:
    return sorted(circle, key=lambda d: d[-1], reverse=True)


def circles_sort_p2p(circle):
    return sorted(circle, key=lambda d: d["spred"], reverse=True)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages["start_message"].format(message.from_user.first_name))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, messages["help_message"])


@bot.message_handler(commands=['search_spreads'])
def search_spreads(message):
    start_time = time.time()
    bot.send_message(message.chat.id, messages["search_spreads_message"])
    trade = TriangularArbitration("ETH")
    circles = trade.find_spreads()
    circles = circles_sort(circles)
    for circle in circles[:5]:
        bot.send_message(message.chat.id,
                         "*Спред: {0}\n{1} - {2}\n{3} - {4}\n{5} - {6}*".format(circle[-1], circle[0]["symbol"],
                                                                                circle[0]["askPrice"],
                                                                                circle[1]["symbol"],
                                                                                circle[1]["askPrice"],
                                                                                (circle[2])["symbol"],
                                                                                circle[0]["bidPrice"]),
                         parse_mode="Markdown")
    bot.delete_message(message.chat.id, message.id + 1)
    bot.send_message(message.chat.id, "--- %s seconds ---" % (time.time() - start_time))


@bot.message_handler(commands=['search_spreads_p2p'])
def search_spreads_p2p(message):
    start_time = time.time()
    bot.send_message(message.chat.id, messages["search_spred_p2p_message"],)
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
        userNo = f'https://p2p.binance.com/ru/advertiserDetail?advertiserNo={buy["advertiserNo"]}'
        text = messages["spred_p2p_message"].format(buy_banks, buy_asset, buy_price, sell_banks, sell_price, spred, userNo)
        bot.send_message(message.chat.id, text, parse_mode="MarkdownV2", disable_web_page_preview=True)
    bot.delete_message(message.chat.id, message.id + 1)
    bot.send_message(message.chat.id, "--- %s seconds ---" % (time.time() - start_time))


bot.polling()

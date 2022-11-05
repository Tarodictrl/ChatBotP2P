import threading
from config import *
import telebot
from telebot import types
import json
from binanceparser import *
import time

bot = telebot.TeleBot(BOT_TOKEN)

with open("messages.json", encoding="utf-8") as f: messages = json.load(f)


def circles_sort(circle: list) -> list:
    return sorted(circle, key=lambda d: d['spred'], reverse=True)


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
    trade = Trade("USDT", "BTC", 1000)
    bundles = trade.get_bundles()
    for bundle in bundles[:10]:
        base = bundle[0]
        trade.buy()
        trade.sell(base)
        trade.end_circle()
        trade.reset()

    circles = circles_sort(trade.get_circles())[:5]
    for t in circles:
        circle = f'{t["1"]} -> {t["2"]} -> {t["3"]}'
        spred = t["spred"]
        spred_p = t["spred_p"]
        bot.send_message(message.chat.id, text=messages["spred_message"].format(spred, spred_p, circle), parse_mode="Markdown")
    bot.delete_message(message.chat.id, message.id+1)
    bot.send_message(message.chat.id, "--- %s seconds ---" % (time.time() - start_time))


bot.infinity_polling()

import json
import time
from config import *
import telebot
from binanceparser import *

bot = telebot.TeleBot(BOT_TOKEN)

with open("messages.json", encoding="utf-8") as f: messages = json.load(f)


def circles_sort(circle: list) -> list:
    return sorted(circle, key=lambda d: d[-1], reverse=True)


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
    trade = TriangularArbitration("USDT")
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


bot.infinity_polling()

import logging
import re
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, filters
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None)

logging.basicConfig(level=logging.INFO)

def normalize_query(text):
    return re.sub(r"[^\w\d\-\/\.]", "", text)

def search_ebay_prices(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(
        f"https://www.ebay.com/sch/i.html?_nkw={query}&LH_BIN=1",
        headers=headers,
    )

    prices = re.findall(r"\$\d{1,6}(?:\.\d{2})?", response.text)
    prices = [float(p.replace("$", "")) for p in prices[:10]]

    if not prices:
        return "Цены на eBay не найдены."

    return (
        f"По eBay:\n"
        f"- Мин. цена: ${min(prices)}\n"
        f"- Средняя цена: ${round(sum(prices)/len(prices), 2)}\n"
        f"- Последняя цена: ${prices[0]}"
    )

def handle_message(update: Update, context):
    query = normalize_query(update.message.text.strip())
    result = search_ebay_prices(query)
    update.message.reply_text(result)

dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/")
def index():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "ok"

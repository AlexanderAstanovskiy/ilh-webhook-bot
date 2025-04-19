import requests
import re
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def normalize_query(query):
    return ''.join(c for c in query if c.isalnum() or c in '-/.')

def search_ebay_prices(query):
    try:
        search_query = normalize_query(query)
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        items = response.text.split("$")[1:]
        prices = []

        for item in items[:10]:
            match = re.match(r"([0-9]+\.[0-9]+)", item)
            if match:
                prices.append(float(match.group(1)))

        if not prices:
            return "Цены на eBay не найдены."

        min_price = min(prices)
        avg_price = round(sum(prices) / len(prices), 2)
        last_price = prices[-1]

        return (
            f"По eBay:\n"
            f"- Мин. цена: ${min_price}\n"
            f"- Средняя цена: ${avg_price}\n"
            f"- Последняя цена: ${last_price}"
        )

    except Exception as e:
        return f"Ошибка при поиске: {e}"

def handle_message(update: Update, context):
    query = update.message.text
    result = search_ebay_prices(query)
    update.message.reply_text(result)

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "ok"

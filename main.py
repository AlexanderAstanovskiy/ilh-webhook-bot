import requests
import re
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters

TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"
bot = Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None)

def normalize_query(query):
    return ''.join(c for c in query if c.isalnum())

def search_ebay_prices(query):
    try:
        search_query = normalize_query(query)
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        items = response.text.split(">")
        prices = re.findall(r"\$\d{1,6}(\.\d{1,2})?", response.text)
        prices = [float(p.replace("$", "")) for p in prices if "$" in p]

        if not prices:
            return "Цены на eBay не найдены."

        return (
            f"По eBay:\n"
            f"- Мин. цена: ${min(prices)}\n"
            f"- Средняя цена: ${round(sum(prices)/len(prices), 2)}\n"
            f"- Последняя цена: ${prices[-1]}"
        )
    except Exception as e:
        return f"Ошибка поиска: {str(e)}"

def handle_message(update: Update, context):
    query = update.message.text.strip()
    result = search_ebay_prices(query)
    update.message.reply_text(result)

dispatcher.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.route("/")
def index():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "ok"

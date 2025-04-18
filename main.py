import logging
import re
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, filters, CallbackContext
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN", "твой_токен_сюда")
bot = Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

logging.basicConfig(level=logging.INFO)

def normalize_query(text):
    return re.sub(r"[^A-Za-z0-9\-]", "", text.strip())

def search_ebay_prices(query):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sop=12"
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

        prices = [float(p.replace(",", "").replace("$", "")) for p in re.findall(r"\$\d{1,6}(?:,\d{3})*(?:\.\d{1,2})?", html)]
        prices = [p for p in prices if p > 0]

        if not prices:
            return "Цены на eBay не найдены."

        return (
            f"По eBay:\n"
            f"- Минимальная цена: ${min(prices)}\n"
            f"- Средняя цена: ${round(sum(prices)/len(prices), 2)}\n"
            f"- Последняя цена: ${prices[0]}"
        )
    except Exception as e:
        return f"Ошибка при поиске: {str(e)}"

def handle_message(update: Update, context: CallbackContext):
    query = normalize_query(update.message.text)
    result = search_ebay_prices(query)
    update.message.reply_text(result)

@app.route('/')
def index():
    return "Bot is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "ok"

dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def search_ebay_prices(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    prices = []

    for item in soup.select(".s-item"):
        price_span = item.select_one(".s-item__price")
        if price_span:
            price_text = price_span.text.replace("$", "").replace(",", "").strip()
            try:
                price = float(price_text.split()[0])
                prices.append(price)
            except:
                continue

    if not prices:
        return "Цены на eBay не найдены."

    min_price = min(prices)
    avg_price = round(sum(prices) / len(prices), 2)
    last_price = prices[0]

    return (
        f"По eBay:\n"
        f"- Минимальная цена: ${min_price}\n"
        f"- Средняя цена: ${avg_price}\n"
        f"- Последняя цена: ${last_price}"
    )

def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    ebay_result = search_ebay_prices(query)
    update.message.reply_text(ebay_result)

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route('/')
def index():
    return "Bot is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

import requests
import re
from flask import Flask, request

TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def normalize_query(query):
    return ''.join(c for c in query if c.isalnum() or c in "-_/")

def search_ebay_prices(query):
    try:
        search_query = normalize_query(query)
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        items = response.text.split("$")
        prices = []

        for item in items[1:]:
            price = re.findall(r"\d{1,5}\.\d{2}", item)
            if price:
                prices.append(float(price[0]))

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

@app.route("/")
def index():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        query = data["message"]["text"]
        result = search_ebay_prices(query)
        requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": result})
    return "ok"

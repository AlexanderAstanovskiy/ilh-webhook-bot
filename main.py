import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def normalize_query(query):
    return ''.join(c for c in query if c.isalnum())

def search_ebay_prices(query):
    try:
        search_query = normalize_query(query)
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}&LH_BIN=1"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        items = response.text.split('s-item__price')[1:11]

        prices = []
        for item in items:
            start = item.find('$') + 1
            end = item.find('<', start)
            if start > 0 and end > start:
                price_str = item[start:end].replace(",", "")
                try:
                    price = float(price_str)
                    if price > 20:
                        prices.append(price)
                except:
                    continue

        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = round(sum(prices) / len(prices), 2)
            return f"Минимальная: ${min_price}\nСредняя: ${avg_price}\nМаксимальная: ${max_price}"
        else:
            return "Цены не найдены или все предложения ниже $20."
    except Exception as e:
        return f"Ошибка при поиске: {e}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        query = data["message"]["text"]
        result = search_ebay_prices(query)
        payload = {"chat_id": chat_id, "text": result}
        requests.post(URL, json=payload)
    return {"ok": True}

@app.route("/")
def home():
    return "Bot is running"

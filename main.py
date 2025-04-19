import os
import requests
from flask import Flask, request

app = Flask(__name__)
TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def search_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    return f"Поиск на eBay: {url}"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        search_result = search_ebay(text.strip())
        requests.post(TELEGRAM_URL, data={"chat_id": chat_id, "text": search_result})
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import os
import requests
from flask import Flask, request
import telegram
from urllib.parse import quote_plus

TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram bot is running"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    query = update.message.text.strip()

    response = deep_search_prices(query)
    bot.send_message(chat_id=chat_id, text=response, parse_mode=telegram.ParseMode.HTML)
    return 'ok'

def deep_search_prices(query):
    query_encoded = quote_plus(query)

    urls = [
        f"https://www.ebay.com/sch/i.html?_nkw={query_encoded}",
        f"https://www.google.com/search?q=site%3A{detect_brand_site(query)}+{query_encoded}",
        f"https://www.aliexpress.com/wholesale?SearchText={query_encoded}",
        f"https://s.taobao.com/search?q={query_encoded}",
        f"https://www.google.com/search?q={query_encoded}+site%3A.cn",
        f"https://www.google.com/search?q={query_encoded}+site%3A.de",
        f"https://www.google.com/search?q={query_encoded}+site%3A.com"
    ]

    sources = [
        "eBay",
        "Manufacturer",
        "AliExpress",
        "Taobao",
        "China",
        "Europe",
        "USA"
    ]

    results = []
    for url, name in zip(urls, sources):
        results.append(f"<b>{name}</b>: <a href=\"{url}\">{url}</a>")

    return "\n\n".join(results)

def detect_brand_site(query):
    query_lower = query.lower()
    brands = {
        "festo": "festo.com",
        "bosch rexroth": "boschrexroth.com",
        "siemens": "new.siemens.com",
        "balluff": "balluff.com",
        "hydac": "hydac.com",
        "honeywell": "honeywell.com",
        "parker": "parker.com",
        "bonfiglioli": "bonfiglioli.com",
        "sew-eurodrive": "sew-eurodrive.com",
        "abb": "abb.com",
        "aventics": "aventics.com",
        "bronkhorst": "bronkhorst.com",
        "sick": "sick.com",
        "smc": "smc.eu"
    }
    for key in brands:
        if key in query_lower:
            return brands[key]
    return "google.com"

if __name__ == '__main__':
    app.run(debug=True)

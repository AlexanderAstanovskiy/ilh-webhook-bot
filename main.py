from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
import requests
from bs4 import BeautifulSoup

TOKEN = "ТВОЙ_ТОКЕН_ЗДЕСЬ"
BOT_URL = "https://ilh-webhook-bot.onrender.com"

app = Flask(__name__)

def search_ebay(query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("li.s-item")
        results = []
        for item in items[:3]:
            title = item.select_one("h3")
            price = item.select_one(".s-item__price")
            link = item.select_one("a")
            if title and price and link:
                results.append(f"{title.text} — {price.text}\n{link['href']}")
        if results:
            return "\n\n".join(results)
        else:
            return "Цены на eBay не найдены."
    except Exception as e:
        return f"Ошибка при поиске на eBay: {e}"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook(request=request):
    data = request.get_json(force=True)
    update = Update.de_json(data, Application.builder().token(TOKEN).build().bot)
    await application.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!"

application = Application.builder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, ctx: update.message.reply_text(search_ebay(update.message.text))))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def search_ebay(query: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".s-item")
        prices = [item.select_one(".s-item__price") for item in items if item.select_one(".s-item__price")]
        if not prices:
            return "Цены на eBay не найдены."
        return f"Минимальная цена на eBay: {prices[0].text.strip()}"
    except Exception as e:
        return f"Ошибка при поиске на eBay: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text.strip()
    result = await search_ebay(query)
    await update.message.reply_text(result)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT")),
        webhook_url="https://ilh-webhook-bot-1.onrender.com"
    )

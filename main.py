import os
import logging
import httpx
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def search_ebay(query: str) -> str:
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".s-item .s-item__price")
        prices = [item.get_text(strip=True) for item in items]

        if not prices:
            return "Цены на eBay не найдены."
        return f"Минимальная цена на eBay: {prices[0]}"
    except Exception as e:
        return f"Ошибка при поиске на eBay: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    result = await search_ebay(query)
    await update.message.reply_text(result)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT")),
        webhook_url="https://ilh-webhook-bot.onrender.com"
    )

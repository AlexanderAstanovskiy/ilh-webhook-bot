import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# eBay-поиск — выдаёт минимальную цену по запросу
async def search_ebay(query: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sop=15"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".s-item")
        prices = [item.select_one(".s-item__price") for item in items if item.select_one(".s-item__price")]
        if not prices:
            return "Цены на eBay не найдены."
        return f"Минимальная цена на eBay: {prices[0].text}"
    except Exception as e:
        return f"Ошибка при поиске на eBay: {e}"

# Обработка входящего сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    logging.info(f"Получен запрос: {query}")
    result = await search_ebay(query)
    logging.info(f"Ответ пользователю: {result}")
    await update.message.reply_text(result)

# Запуск приложения
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT")),
        webhook_url="https://ilh-webhook-bot-1.onrender.com"
    )

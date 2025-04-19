import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# eBay поиск — выдаёт минимальную цену с eBay
async def search_ebay(query: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".s-item")

        prices = []
        for item in items:
            price_tag = item.select_one(".s-item__price")
            link_tag = item.select_one(".s-item__link")
            if price_tag and link_tag:
                price_text = price_tag.get_text().replace(",", "").replace("$", "")
                try:
                    price = float(price_text.split()[0])
                    prices.append((price, link_tag["href"]))
                except ValueError:
                    continue

        if not prices:
            return "Цены на eBay не найдены."

        prices.sort(key=lambda x: x[0])
        min_price, link = prices[0]
        return f"Минимальная цена на eBay: ${min_price} \n{link}"

    except Exception as e:
        logging.error(f"Ошибка при поиске на eBay: {e}")
        return "Ошибка при поиске на eBay."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправьте артикул для поиска на eBay.")

# Обработка текста
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text(f"Вы ввели: {query}")
    result = await search_ebay(query)
    await update.message.reply_text(result)

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", default=10000)),
        webhook_url="https://ilh-webhook-bot-1.onrender.com/"
    )

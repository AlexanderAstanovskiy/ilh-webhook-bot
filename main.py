import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get('PORT', 10000))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите артикул для поиска на eBay:")

async def search_ebay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text(f"Вы ввели: {query}")

    ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={requests.utils.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(ebay_url, headers=headers)

    if "results" in response.text.lower():
        await update.message.reply_text("Цены на eBay не найдены.")
    else:
        await update.message.reply_text(f"Возможно, найдены предложения:\n{ebay_url}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_ebay))
    app.run_polling(port=PORT, allowed_updates=Update.ALL_TYPES)

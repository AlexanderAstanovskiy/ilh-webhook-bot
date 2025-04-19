import os
import logging
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# Вставляем токен
BOT_TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Создание Flask
app = Flask(__name__)

# Функция обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
    await update.message.reply_text(f"Поиск на eBay:\n{url}")

# Настройка Telegram Application
telegram_app = Application.builder().token(BOT_TOKEN).build()
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask endpoint для webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"

# Главная страница
@app.route("/")
def index():
    return "Бот работает!"

# Запуск
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"https://ilh-webhook-bot.onrender.com/{BOT_TOKEN}"
    )

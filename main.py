import logging
import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters, CallbackContext

# Твой токен Telegram
BOT_TOKEN = "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc"

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создание Flask-приложения
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# Инициализация диспетчера
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# Обработчик сообщений
def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
    update.message.reply_text(f"Вот ссылка на поиск eBay:\n{ebay_url}")

# Привязка обработчика
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook для Telegram
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Корневая страница
@app.route("/")
def index():
    return "Бот запущен и работает."

# Запуск приложения
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

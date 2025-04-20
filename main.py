from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.environ.get("BOT_TOKEN", "7671684242:AAH4CjpaNdzz5dFu0iN7qYKgdDN3uaiaKgc")

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне артикул, и я найду цену на eBay.")

application.add_handler(CommandHandler("start", start))

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

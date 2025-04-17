import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

@app.route('/')
def index():
    return "Bot is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

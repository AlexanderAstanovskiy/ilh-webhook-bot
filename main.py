
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "")
    return {"response": f"Вы ввели: {message}"}

if __name__ == "__main__":
    app.run(debug=True)

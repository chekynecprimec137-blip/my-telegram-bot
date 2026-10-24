import telebot
from flask import Flask
from threading import Thread
import os

# --- Сайт для Render ---
app = Flask('')

@app.route('/')
def home():
    return "Бот работает 24/7!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Твой бот ---
bot = telebot.TeleBot("8695726820:AAES_PN9Ajz7Pq39yKJplsxIMFQExAYHFjA")
ADMIN_ID = 8745598065

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Привет! Я работаю в облаке 24/7.")
    else:
        bot.send_message(message.chat.id, "Привет! Напиши сообщение, и я передам его.")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.chat.id == ADMIN_ID:
        if message.reply_to_message:
            try:
                text = message.reply_to_message.text
                user_id = int(text.split('ID: ')[1].split('\n')[0])
                bot.send_message(user_id, f"Ответ:\n\n{message.text}")
            except Exception:
                pass
    else:
        bot.send_message(ADMIN_ID, f"ID: {message.chat.id}\n\n{message.text}")
        bot.send_message(message.chat.id, "Отправлено!")

keep_alive()
bot.infinity_polling()

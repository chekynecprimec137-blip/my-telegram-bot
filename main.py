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
bot = telebot.TeleBot("8695726820:AAE_j0u02fQ9JUi5u3s9rwbv7kxxWztPO2M")
ADMIN_ID = 8745598065

# Тут храним забаненных (черный список)
banned_users = set() 

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Привет! Я работаю в облаке 24/7.")
    else:
        bot.send_message(message.chat.id, "Привет! Напиши сообщение, и я передам его создателю.")

# --- Команда для бана ---
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.id == ADMIN_ID:
        if message.reply_to_message:
            try:
                # Берем ID из сообщения, на которое ты ответил
                text = message.reply_to_message.text
                user_id = int(text.split('ID: ')[1].split('\n')[0])
                
                banned_users.add(user_id) # Добавляем в черный список
                bot.send_message(ADMIN_ID, f"✅ Пользователь {user_id} заблокирован. Теперь он в игноре.")
            except Exception:
                bot.send_message(ADMIN_ID, "⚠️ Ошибка. Зажми сообщение с 'ID: ...' и напиши /ban.")
        else:
            bot.send_message(ADMIN_ID, "⚠️ Чтобы забанить, зажми сообщение нарушителя, выбери 'Ответить' и напиши /ban.")

# --- Обработка сообщений ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Проверяем, не забанен ли этот человек
    if message.chat.id in banned_users:
        return # Если забанен - просто игнорируем

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

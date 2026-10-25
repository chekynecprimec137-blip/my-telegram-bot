import telebot
from flask import Flask
from threading import Thread
import os

# --- Сайт для Render (чтобы не засыпал) ---
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
# ВСТАВЬ СВОЙ НОВЫЙ ТОКЕН (в кавычках)
bot = telebot.TeleBot("8695726820:AAGBFeXpdDwMxcrnz18NgG97f5YUBUYeUxo")

# Твой ID уже вписан
ADMIN_ID = 8745598065 

# Черный список для спамеров
banned_users = set() 

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Привет, создатель! Я работаю в облаке 24/7.")
    else:
        bot.send_message(message.chat.id, "Привет! Напиши сообщение, и я передам его создателю.")

@bot.message_handler(commands=['help'])
def help_command(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Твои команды:\n/start - статус\n/ban - забанить (через Reply на сообщение с ID)\n/help - это меню")
    else:
        bot.send_message(message.chat.id, "Привет! Просто напиши сюда любое сообщение, и я анонимно передам его Создателю.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.id == ADMIN_ID:
        if message.reply_to_message:
            try:
                text = message.reply_to_message.text
                user_id = int(text.split('ID: ')[1].split('\n')[0])
                banned_users.add(user_id) 
                bot.send_message(ADMIN_ID, f"✅ Пользователь {user_id} заблокирован. Теперь он в игноре.")
            except Exception:
                bot.send_message(ADMIN_ID, "⚠️ Ошибка. Зажми сообщение с 'ID: ...' и напиши /ban.")
        else:
            bot.send_message(ADMIN_ID, "⚠️ Чтобы забанить, зажми сообщение нарушителя, выбери 'Ответить' и напиши /ban.")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Проверяем, не забанен ли человек
    if message.chat.id in banned_users:
        return # Игнорируем забаненных

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
        bot.send_message(message.chat.id, "✅ Отправлено!")

keep_alive()
bot.infinity_polling()

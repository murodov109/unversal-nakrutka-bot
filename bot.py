from telebot import TeleBot, types
from flask import Flask
import threading
import time
import random

from config import TOKEN, ADMINS
from db import Database
import admin_panel
import user_panel
import orders
import payments

bot = TeleBot(TOKEN)
db = Database()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishga tushdi."

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    db.add_user(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 Buyurtma berish", "💰 Pul ishlash")
    markup.add("🎁 Kunlik bonus", "ℹ️ Hisobim")
    if user_id in ADMINS:
        markup.add("🧩 Admin panel")
    text = ("👋 Salom, bu yerda siz kanal va botlaringizni tezda rivojlantira olasiz!\n\n"
            "🛒 Buyurtma bering, yoki 💰 Pul ishlash tugmasi orqali do‘stlaringizni taklif qilib daromad oling!")
    bot.send_message(user_id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🧩 Admin panel")
def open_admin(message):
    if message.from_user.id in ADMINS:
        admin_panel.show_admin_panel(bot, message, db)
    else:
        bot.reply_to(message, "⛔ Sizda bu bo‘limga kirish huquqi yo‘q.")

@bot.message_handler(func=lambda message: message.text == "💰 Pul ishlash")
def earn_money(message):
    user_panel.show_referral_panel(bot, message, db)

@bot.message_handler(func=lambda message: message.text == "🎁 Kunlik bonus")
def daily_bonus(message):
    user_id = message.from_user.id
    if db.can_get_bonus(user_id):
        amount = random.randint(10, 100)
        db.add_balance(user_id, amount)
        db.update_bonus_time(user_id)
        bot.reply_to(message, f"🎉 Tabriklaymiz! Siz bugun {amount} so‘m bonus oldingiz.")
    else:
        bot.reply_to(message, "⏳ Siz bugungi bonusni allaqachon olgansiz. Ertaga yana urinib ko‘ring.")

@bot.message_handler(func=lambda message: message.text == "🛒 Buyurtma berish")
def make_order(message):
    orders.start_order(bot, message, db)

@bot.message_handler(func=lambda message: message.text == "ℹ️ Hisobim")
def my_account(message):
    user_panel.show_user_info(bot, message, db)

@bot.message_handler(func=lambda message: message.text == "💳 To‘lovlar")
def payments_menu(message):
    payments.show_payments_panel(bot, message, db)

if __name__ == "__main__":
    keep_alive()
    print("✅ Bot ishga tushdi...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print("Xatolik:", e)
            time.sleep(3)

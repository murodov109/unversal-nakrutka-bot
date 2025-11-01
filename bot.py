import telebot
from telebot import types
from config import BOT_TOKEN
from keep_alive import keep_alive
from user_panel import handle_user_panel
from admin_panel import handle_admin_panel
from db import Database

bot = telebot.TeleBot(BOT_TOKEN)
db = Database()

keep_alive()

@bot.message_handler(commands=['start'])
def start(message):
    db.add_user(message.from_user.id, message.from_user.username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💸 Pul ishlash", "🛍 Buyurtma berish")
    markup.add("💰 Hisobim", "➕ Hisobni to‘ldirish")
    markup.add("📋 Vazifalar", "🎁 Kunlik bonus")
    bot.send_message(message.chat.id, f"👋 Salom, {message.from_user.first_name}!\nBotga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    user_id = message.from_user.id
    text = message.text

    if text == "💸 Pul ishlash":
        handle_user_panel(bot, message)
    elif text == "🛍 Buyurtma berish":
        bot.send_message(user_id, "💬 Buyurtma berish bo‘limi ishga tushmoqda...")
    elif text == "💰 Hisobim":
        balance = db.get_balance(user_id)
        bot.send_message(user_id, f"💵 Sizning hisobingizda: {balance} so‘m bor.")
    elif text == "➕ Hisobni to‘ldirish":
        bot.send_message(user_id, "💳 Hisobni to‘ldirish uchun kartaga to‘lov yuboring.")
    elif text == "📋 Vazifalar":
        bot.send_message(user_id, "📢 Mavjud vazifalar ro‘yxati tez orada qo‘shiladi.")
    elif text == "🎁 Kunlik bonus":
        bot.send_message(user_id, "🎲 Kunlik bonus funksiyasi hozircha testda!")
    elif text.startswith("/admin"):
        handle_admin_panel(bot, message)
    else:
        bot.send_message(user_id, "⚠️ Tugmalardan birini tanlang.")

bot.polling(none_stop=True)

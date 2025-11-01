import telebot
from telebot import types
import random
from config import BOT_TOKEN, ADMINS
from db import add_user, get_balance, add_balance, get_random_user
from admin_panel import handle_admin_commands, send_admin_panel, is_admin

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"
    add_user(user_id, username)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Balans", "🎁 Kunlik bonus", "👑 Admin panel")
    bot.send_message(user_id, f"👋 Salom, {username}!\nSiz tizimga muvaffaqiyatli kirdingiz.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 Balans")
def balance(message):
    user_id = message.from_user.id
    bal = get_balance(user_id)
    bot.send_message(user_id, f"💵 Sizning balansingiz: {bal} so‘m")

@bot.message_handler(func=lambda message: message.text == "🎁 Kunlik bonus")
def daily_bonus(message):
    user_id = message.from_user.id
    bonus = random.randint(10, 100)
    add_balance(user_id, bonus)
    bot.send_message(user_id, f"🎉 Tabriklaymiz! Siz {bonus} so‘m bonus yutdingiz!")

@bot.message_handler(func=lambda message: message.text == "👑 Admin panel")
def admin_panel(message):
    user_id = message.from_user.id
    if user_id in ADMINS or is_admin(user_id):
        send_admin_panel(bot, user_id)
    else:
        bot.send_message(user_id, "🚫 Sizda admin huquqi yo‘q.")

@bot.message_handler(content_types=['text'])
def handle_all(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        handle_admin_commands(bot, message)
    else:
        bot.send_message(user_id, "❗ Noma’lum buyruq. Asosiy menyudan foydalaning.")

bot.polling(none_stop=True)

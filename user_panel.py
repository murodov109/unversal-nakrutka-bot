import telebot
from telebot import types
from db import Database
import random

db = Database()

def handle_user_panel(bot, message):
    user_id = message.from_user.id
    username = message.from_user.username or "Foydalanuvchi"

    markup = types.InlineKeyboardMarkup()
    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    markup.add(types.InlineKeyboardButton("👥 Referal havolam", url=ref_link))
    markup.add(types.InlineKeyboardButton("🎁 Kunlik bonus olish", callback_data="daily_bonus"))
    bot.send_message(user_id, "💸 Pul ishlash bo‘limi:\n\n👇 Quyidagi havolani do‘stlaringizga yuboring va har bir taklif uchun 300 so‘m oling!", reply_markup=markup)

@staticmethod
def send_bonus(bot, call):
    user_id = call.from_user.id
    if db.can_take_bonus(user_id):
        bonus = random.randint(10, 100)
        db.add_balance(user_id, bonus)
        db.set_bonus_taken(user_id)
        bot.answer_callback_query(call.id, f"🎉 Siz {bonus} so‘m bonus oldingiz!")
    else:
        bot.answer_callback_query(call.id, "⏳ Siz bonusni kuniga bir marta olishingiz mumkin!")

def handle_callback(bot, call):
    if call.data == "daily_bonus":
        send_bonus(bot, call)

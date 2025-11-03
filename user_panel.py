import telebot
from telebot import types
from config import REF_BONUS, BONUS_MIN, BONUS_MAX
from db import Database
import random
import time

db = Database("data.db")

# Foydalanuvchi menyusi
def handle_user_panel(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Balans", "🎁 Bonus olish")
    markup.add("👥 Referal tizimi", "🛒 Buyurtma berish")
    markup.add("📞 Yordam")

    bot.send_message(
        message.chat.id,
        f"Salom, {message.from_user.first_name}! 👋\nQuyidagi menyudan birini tanlang:",
        reply_markup=markup
    )

# Balansni ko‘rsatish
def show_balance(bot, message):
    user = db.get_user(message.chat.id)
    if user:
        bot.send_message(message.chat.id, f"💰 Sizning balansingiz: {user[3]:.2f} so‘m")
    else:
        bot.send_message(message.chat.id, "Siz ro‘yxatdan o‘tmagansiz. /start ni bosing!")

# Bonus olish
def get_bonus(bot, message):
    user = db.get_user(message.chat.id)
    if not user:
        bot.send_message(message.chat.id, "Avval /start buyrug‘ini bosing!")
        return

    now = int(time.time())
    last_bonus_time = user[4] if len(user) > 4 else 0
    if now - last_bonus_time < 86400:  # 24 soat
        remaining = 86400 - (now - last_bonus_time)
        bot.send_message(message.chat.id, f"🎁 Siz bonusni allaqachon olgansiz.\nYangi bonus {remaining // 3600} soatdan keyin.")
        return

    bonus_amount = random.randint(BONUS_MIN, BONUS_MAX)
    db.add_balance(message.chat.id, bonus_amount)
    db.set_bonus_time(message.chat.id, now)

    bot.send_message(message.chat.id, f"🎉 Tabriklaymiz! Siz {bonus_amount} so‘m bonus oldingiz.")

# Referal tizimi
def referral_info(bot, message):
    ref_link = f"https://t.me/{bot.get_me().username}?start={message.chat.id}"
    bot.send_message(
        message.chat.id,
        f"👥 Sizning referal linkingiz:\n{ref_link}\n\n"
        f"Do‘stlaringiz ushbu link orqali kirsa, siz {REF_BONUS} so‘m olasiz!"
    )

# Buyurtma berish
def make_order(bot, message):
    bot.send_message(
        message.chat.id,
        "🛒 Buyurtma berish funksiyasi hozircha ishlab chiqilmoqda.\nTez orada ishga tushadi!"
    )

# Yordam
def help_info(bot, message):
    bot.send_message(
        message.chat.id,
        "📞 Yordam uchun admin bilan bog‘laning:\n@admin_username"
    )

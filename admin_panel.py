import telebot
from telebot import types
from db import Database
from config import ADMINS

db = Database()

def handle_admin_panel(bot, message):
    if message.from_user.id not in ADMINS:
        bot.send_message(message.chat.id, "🚫 Sizda admin huquqi yo‘q!")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Statistika", "💵 Foydalanuvchi hisobiga pul qo‘shish")
    markup.add("➕ Kanal qo‘shish", "➖ Kanalni o‘chirish")
    markup.add("💬 Reklama yuborish", "👑 Admin qo‘shish")
    markup.add("⬅️ Asosiy menyuga qaytish")

    bot.send_message(message.chat.id, "👑 Admin panelga xush kelibsiz!", reply_markup=markup)

@staticmethod
def admin_menu(bot, message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in ADMINS:
        bot.send_message(user_id, "❌ Siz admin emassiz.")
        return

    if text == "📊 Statistika":
        users = db.get_users()
        admins = db.get_admins()
        bot.send_message(user_id, f"📈 Statistika:\n👥 Foydalanuvchilar: {len(users)} ta\n👑 Adminlar: {len(admins)} ta")

    elif text == "💵 Foydalanuvchi hisobiga pul qo‘shish":
        bot.send_message(user_id, "✏️ Foydalanuvchi ID raqamini yuboring:")
        bot.register_next_step_handler(message, lambda msg: ask_amount(bot, msg))

    elif text == "➕ Kanal qo‘shish":
        bot.send_message(user_id, "📢 Kanal ID sini yuboring (masalan: -1001234567890):")
        bot.register_next_step_handler(message, lambda msg: add_channel(bot, msg))

    elif text == "➖ Kanalni o‘chirish":
        bot.send_message(user_id, "❌ O‘chirmoqchi bo‘lgan kanal ID sini yuboring:")
        bot.register_next_step_handler(message, lambda msg: remove_channel(bot, msg))

    elif text == "💬 Reklama yuborish":
        bot.send_message(user_id, "📣 Reklama matnini yuboring:")
        bot.register_next_step_handler(message, lambda msg: send_ad(bot, msg))

    elif text == "👑 Admin qo‘shish":
        bot.send_message(user_id, "🆔 Admin ID raqamini yuboring:")
        bot.register_next_step_handler(message, lambda msg: add_admin(bot, msg))

def ask_amount(bot, message):
    try:
        user_id = int(message.text)
        bot.send_message(message.chat.id, "💰 Qancha pul qo‘shmoqchisiz?")
        bot.register_next_step_handler(message, lambda msg: add_balance(bot, user_id, msg))
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID raqami.")

def add_balance(bot, user_id, message):
    try:
        amount = int(message.text)
        db.add_balance(user_id, amount)
        bot.send_message(message.chat.id, f"✅ {user_id} foydalanuvchisiga {amount} so‘m qo‘shildi.")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri miqdor.")

def add_channel(bot, message):
    try:
        channel_id = int(message.text)
        db.add_channel(channel_id)
        bot.send_message(message.chat.id, f"✅ Kanal qo‘shildi: {channel_id}")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri kanal ID.")

def remove_channel(bot, message):
    try:
        channel_id = int(message.text)
        db.remove_channel(channel_id)
        bot.send_message(message.chat.id, f"🗑 Kanal o‘chirildi: {channel_id}")
    except:
        bot.send_message(message.chat.id, "❌ Xato kanal ID.")

def send_ad(bot, message):
    text = message.text
    users = db.get_users()
    for user in users:
        try:
            bot.send_message(user, text)
        except:
            continue
    bot.send_message(message.chat.id, "✅ Reklama barcha foydalanuvchilarga yuborildi.")

def add_admin(bot, message):
    try:
        admin_id = int(message.text)
        db.add_admin(admin_id)
        bot.send_message(message.chat.id, f"👑 Yangi admin qo‘shildi: {admin_id}")
    except:
        bot.send_message(message.chat.id, "❌ Xato ID.")

from telebot import types
from db import get_users, add_balance, update_card, add_task, get_random_user, get_channels, add_channel, remove_channel, add_admin, get_admins
from config import ADMINS, BOT_USERNAME, CARD_NUMBER
import random

def admin_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Statistika", "➕ Vazifa qo‘shish")
    markup.add("💳 Karta raqamni o‘zgartirish", "👑 Omadli foydalanuvchi")
    markup.add("📢 Reklama tarqatish", "💰 Foydalanuvchi hisobiga pul qo‘shish")
    markup.add("📡 Majburiy kanallar", "👮 Admin qo‘shish")
    bot.send_message(message.chat.id, "🛠 Admin paneliga xush kelibsiz!", reply_markup=markup)

def handle_admin(bot, message):
    if str(message.chat.id) not in ADMINS:
        bot.send_message(message.chat.id, "⛔ Siz admin emassiz.")
        return

    if message.text == "📊 Statistika":
        users = get_users()
        total_users = len(users)
        active_users = sum(1 for u in users if u.get("active"))
        bot.send_message(message.chat.id, f"📈 Jami foydalanuvchilar: {total_users}\n🟢 Aktivlar: {active_users}")

    elif message.text == "💳 Karta raqamni o‘zgartirish":
        msg = bot.send_message(message.chat.id, "💳 Yangi karta raqamini kiriting:")
        bot.register_next_step_handler(msg, lambda m: update_card_handler(bot, m))

    elif message.text == "➕ Vazifa qo‘shish":
        msg = bot.send_message(message.chat.id, "📝 Yangi vazifa matnini yuboring:")
        bot.register_next_step_handler(msg, lambda m: add_task_handler(bot, m))

    elif message.text == "💰 Foydalanuvchi hisobiga pul qo‘shish":
        msg = bot.send_message(message.chat.id, "💬 Foydalanuvchi ID raqamini yuboring:")
        bot.register_next_step_handler(msg, lambda m: add_balance_step1(bot, m))

    elif message.text == "👑 Omadli foydalanuvchi":
        lucky = get_random_user()
        if lucky:
            bot.send_message(message.chat.id, f"🎉 Bugungi omadli foydalanuvchi: @{lucky.get('username')} (ID: {lucky.get('id')})")
        else:
            bot.send_message(message.chat.id, "Foydalanuvchilar topilmadi.")

    elif message.text == "📢 Reklama tarqatish":
        msg = bot.send_message(message.chat.id, "📣 Reklama matnini yuboring:")
        bot.register_next_step_handler(msg, lambda m: send_broadcast(bot, m))

    elif message.text == "📡 Majburiy kanallar":
        show_channels_menu(bot, message)

    elif message.text == "👮 Admin qo‘shish":
        msg = bot.send_message(message.chat.id, "👤 Yangi adminning ID raqamini kiriting:")
        bot.register_next_step_handler(msg, lambda m: add_admin_handler(bot, m))

def update_card_handler(bot, message):
    new_card = message.text.strip()
    update_card(new_card)
    bot.send_message(message.chat.id, f"✅ Karta raqami yangilandi:\n💳 {new_card}")

def add_task_handler(bot, message):
    task = message.text.strip()
    add_task(task)
    bot.send_message(message.chat.id, f"✅ Vazifa qo‘shildi:\n📝 {task}")

def add_balance_step1(bot, message):
    user_id = message.text.strip()
    msg = bot.send_message(message.chat.id, "💰 Miqdorni kiriting:")
    bot.register_next_step_handler(msg, lambda m: add_balance_step2(bot, m, user_id))

def add_balance_step2(bot, message, user_id):
    try:
        amount = int(message.text)
        add_balance(user_id, amount)
        bot.send_message(message.chat.id, f"✅ {user_id} foydalanuvchiga {amount} so‘m qo‘shildi.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri miqdor kiritildi.")

def send_broadcast(bot, message):
    text = message.text
    users = get_users()
    count = 0
    for user in users:
        try:
            bot.send_message(user["id"], f"📢 {text}")
            count += 1
        except:
            continue
    bot.send_message(message.chat.id, f"✅ Reklama {count} ta foydalanuvchiga yuborildi.")

def show_channels_menu(bot, message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ Kanal qo‘shish", callback_data="add_channel"),
               types.InlineKeyboardButton("➖ Kanal o‘chirish", callback_data="remove_channel"))
    channels = get_channels()
    text = "📡 Majburiy kanallar:\n"
    for c in channels:
        text += f"➡️ {c}\n"
    bot.send_message(message.chat.id, text, reply_markup=markup)

def add_admin_handler(bot, message):
    admin_id = message.text.strip()
    add_admin(admin_id)
    bot.send_message(message.chat.id, f"✅ Admin qo‘shildi: {admin_id}")

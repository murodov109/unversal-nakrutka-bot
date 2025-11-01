from telebot import types
from db import add_channel, get_channels, remove_channel, add_balance, get_admins, add_admin

def is_admin(user_id):
    return user_id in get_admins()

def send_admin_panel(bot, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Kanal qo‘shish", "➖ Kanal o‘chirish")
    markup.add("💰 Balans qo‘shish", "👑 Admin qo‘shish")
    bot.send_message(chat_id, "🔐 Admin panelga xush kelibsiz!", reply_markup=markup)

def handle_admin_commands(bot, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.send_message(user_id, "❌ Siz admin emassiz.")
        return

    text = message.text

    if text == "➕ Kanal qo‘shish":
        bot.send_message(user_id, "📢 Kanal ID sini yuboring (masalan: -1001234567890):")
        bot.register_next_step_handler(message, lambda msg: add_new_channel(bot, msg))

    elif text == "➖ Kanal o‘chirish":
        channels = get_channels()
        if not channels:
            bot.send_message(user_id, "⚠️ Hozircha hech qanday kanal yo‘q.")
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for ch in channels:
            markup.add(ch)
        bot.send_message(user_id, "🗑 O‘chirmoqchi bo‘lgan kanalni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: delete_channel(bot, msg))

    elif text == "💰 Balans qo‘shish":
        bot.send_message(user_id, "🆔 Foydalanuvchi ID sini yuboring:")
        bot.register_next_step_handler(message, lambda msg: ask_amount(bot, msg))

    elif text == "👑 Admin qo‘shish":
        bot.send_message(user_id, "🆔 Yangi adminning Telegram ID sini yuboring:")
        bot.register_next_step_handler(message, lambda msg: register_admin(bot, msg))

def add_new_channel(bot, message):
    channel_id = message.text.strip()
    add_channel(channel_id)
    bot.send_message(message.chat.id, f"✅ Kanal qo‘shildi: {channel_id}")

def delete_channel(bot, message):
    channel_id = message.text.strip()
    remove_channel(channel_id)
    bot.send_message(message.chat.id, f"🗑 Kanal o‘chirildi: {channel_id}")

def ask_amount(bot, message):
    user_id = message.text.strip()
    bot.send_message(message.chat.id, "💵 Qo‘shiladigan summa miqdorini yuboring:")
    bot.register_next_step_handler(message, lambda msg: add_money(bot, msg, user_id))

def add_money(bot, message, target_id):
    try:
        amount = float(message.text.strip())
        add_balance(int(target_id), amount)
        bot.send_message(message.chat.id, f"✅ {target_id} foydalanuvchiga {amount} so‘m qo‘shildi.")
    except:
        bot.send_message(message.chat.id, "⚠️ Noto‘g‘ri format. Qayta urinib ko‘ring.")

def register_admin(bot, message):
    try:
        admin_id = int(message.text.strip())
        add_admin(admin_id)
        bot.send_message(message.chat.id, f"👑 Yangi admin qo‘shildi: {admin_id}")
    except:
        bot.send_message(message.chat.id, "⚠️ Noto‘g‘ri ID kiritildi.")

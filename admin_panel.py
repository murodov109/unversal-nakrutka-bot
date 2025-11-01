from telebot import types
from config import bot, ADMINS, CHANNELS
from db import get_user_balance, update_balance, get_all_users, add_admin, remove_admin, get_admins, add_channel, remove_channel, get_channels, get_pending_payments, approve_payment, decline_payment, get_orders, get_total_orders

def admin_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Statistika", "👥 Adminlar", "📢 Kanallar")
    markup.add("💳 To‘lovlar", "📦 Buyurtmalar")
    bot.send_message(chat_id, "🔧 Admin paneliga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📊 Statistika" and message.chat.id in ADMINS)
def stats(message):
    total_users = len(get_all_users())
    total_orders = get_total_orders()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Ortga")
    text = f"📊 Bot statistikasi:\n\n👥 Foydalanuvchilar: {total_users}\n📦 Buyurtmalar: {total_orders}"
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👥 Adminlar" and message.chat.id in ADMINS)
def admins_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Admin qo‘shish", "➖ Admin o‘chirish", "⬅️ Ortga")
    bot.send_message(message.chat.id, "Admin boshqaruvi:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📢 Kanallar" and message.chat.id in ADMINS)
def channels_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Kanal qo‘shish", "➖ Kanal o‘chirish", "⬅️ Ortga")
    bot.send_message(message.chat.id, "Majburiy kanallarni boshqarish:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💳 To‘lovlar" and message.chat.id in ADMINS)
def payments_menu(message):
    payments = get_pending_payments()
    if not payments:
        bot.send_message(message.chat.id, "📭 Hozircha to‘lov so‘rovlari yo‘q.")
        return
    for p in payments:
        user_id, amount, check = p
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{user_id}_{amount}"),
            types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"decline_{user_id}")
        )
        bot.send_photo(message.chat.id, check, caption=f"💳 Foydalanuvchi: {user_id}\n💰 Miqdor: {amount} so‘m", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("decline_"))
def handle_payment_action(call):
    if call.from_user.id not in ADMINS:
        return
    if call.data.startswith("approve_"):
        _, user_id, amount = call.data.split("_")
        user_id = int(user_id)
        amount = int(amount)
        update_balance(user_id, amount)
        approve_payment(user_id)
        bot.send_message(user_id, f"✅ Sizning {amount} so‘mlik to‘lovingiz tasdiqlandi!")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="✅ To‘lov tasdiqlandi!")
    elif call.data.startswith("decline_"):
        _, user_id = call.data.split("_")
        user_id = int(user_id)
        decline_payment(user_id)
        bot.send_message(user_id, "❌ Sizning to‘lov so‘rovingiz rad etildi.")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="❌ To‘lov rad etildi.")

@bot.message_handler(func=lambda message: message.text == "📦 Buyurtmalar" and message.chat.id in ADMINS)
def orders_menu(message):
    orders = get_orders()
    if not orders:
        bot.send_message(message.chat.id, "📦 Hozircha buyurtmalar yo‘q.")
        return
    text = "📦 Buyurtmalar ro‘yxati:\n\n"
    for o in orders:
        text += f"👤 ID: {o[0]} | 💰 {o[1]} so‘m | 🔗 {o[2]}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "➕ Admin qo‘shish" and message.chat.id in ADMINS)
def add_admin_prompt(message):
    bot.send_message(message.chat.id, "➕ Qo‘shmoqchi bo‘lgan admin ID sini yuboring:")
    bot.register_next_step_handler(message, process_add_admin)

def process_add_admin(message):
    try:
        admin_id = int(message.text)
        add_admin(admin_id)
        bot.send_message(message.chat.id, f"✅ Admin {admin_id} qo‘shildi.")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID.")

@bot.message_handler(func=lambda message: message.text == "➖ Admin o‘chirish" and message.chat.id in ADMINS)
def remove_admin_prompt(message):
    bot.send_message(message.chat.id, "🗑 O‘chirmoqchi bo‘lgan admin ID sini yuboring:")
    bot.register_next_step_handler(message, process_remove_admin)

def process_remove_admin(message):
    try:
        admin_id = int(message.text)
        remove_admin(admin_id)
        bot.send_message(message.chat.id, f"✅ Admin {admin_id} o‘chirildi.")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID.")

@bot.message_handler(func=lambda message: message.text == "➕ Kanal qo‘shish" and message.chat.id in ADMINS)
def add_channel_prompt(message):
    bot.send_message(message.chat.id, "📢 Kanal foydalanuvchi nomini yuboring (masalan: @kanal):")
    bot.register_next_step_handler(message, process_add_channel)

def process_add_channel(message):
    ch = message.text.strip()
    add_channel(ch)
    bot.send_message(message.chat.id, f"✅ {ch} kanal majburiy obunaga qo‘shildi.")

@bot.message_handler(func=lambda message: message.text == "➖ Kanal o‘chirish" and message.chat.id in ADMINS)
def remove_channel_prompt(message):
    bot.send_message(message.chat.id, "🗑 O‘chirmoqchi bo‘lgan kanal foydalanuvchi nomini yuboring (masalan: @kanal):")
    bot.register_next_step_handler(message, process_remove_channel)

def process_remove_channel(message):
    ch = message.text.strip()
    remove_channel(ch)
    bot.send_message(message.chat.id, f"✅ {ch} kanal majburiy obunalardan o‘chirildi.")

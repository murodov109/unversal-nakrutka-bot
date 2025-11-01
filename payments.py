from telebot import types
from db import load_data, save_data, get_user_balance, update_user_balance
from config import ADMINS, CARD_NUMBER

pending_payments = {}

def start_payment(bot, message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "💰 Hisobni to‘ldirish uchun miqdorni kiriting (masalan: 10000):")
    bot.register_next_step_handler(message, get_amount, bot)

def get_amount(message, bot):
    chat_id = message.chat.id
    if not message.text.isdigit():
        bot.send_message(chat_id, "❌ Iltimos, raqam kiriting.")
        return start_payment(bot, message)
    amount = int(message.text)
    pending_payments[chat_id] = {"amount": amount}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ To‘lov qildim", callback_data=f"paid_{chat_id}"))
    bot.send_message(chat_id, f"💳 To‘lov uchun karta raqami:\n\n{CARD_NUMBER}\n\n💸 To‘lov summasi: {amount} so‘m\n\nTo‘lovni amalga oshirib, quyidagi tugmani bosing.", reply_markup=markup)

def confirm_payment(bot, call):
    chat_id = call.from_user.id
    if chat_id not in pending_payments:
        bot.answer_callback_query(call.id, "❌ To‘lov topilmadi.")
        return
    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, "📷 To‘lov chekini yuboring:")
    bot.register_next_step_handler_by_chat_id(chat_id, receive_check, bot)

def receive_check(message, bot):
    chat_id = message.chat.id
    if chat_id not in pending_payments:
        bot.send_message(chat_id, "❌ Hech qanday to‘lov topilmadi.")
        return
    if not message.photo:
        bot.send_message(chat_id, "❌ Iltimos, to‘lov chekini rasm shaklida yuboring.")
        return
    amount = pending_payments[chat_id]["amount"]
    file_id = message.photo[-1].file_id
    bot.send_message(chat_id, "🕓 To‘lov arizasi yaratildi. Admin tasdiqlashini kuting.")
    for admin_id in ADMINS:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{chat_id}_{amount}"),
            types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"reject_{chat_id}")
        )
        bot.send_photo(admin_id, file_id, caption=f"💸 Yangi to‘lov arizasi!\n\n👤 ID: {chat_id}\n💰 Miqdor: {amount} so‘m", reply_markup=markup)

def approve_payment(bot, call):
    parts = call.data.split("_")
    user_id = int(parts[1])
    amount = int(parts[2])
    update_user_balance(user_id, amount)
    bot.send_message(user_id, f"✅ To‘lov tasdiqlandi!\nHisobingizga {amount} so‘m qo‘shildi.")
    bot.send_message(call.from_user.id, f"✅ Foydalanuvchi {user_id} uchun to‘lov tasdiqlandi.")
    del pending_payments[user_id]

def reject_payment(bot, call):
    parts = call.data.split("_")
    user_id = int(parts[1])
    bot.send_message(user_id, "❌ To‘lov rad etildi. Agar xato deb o‘ylasangiz, admin bilan bog‘laning.")
    bot.send_message(call.from_user.id, f"❌ Foydalanuvchi {user_id} to‘lovi bekor qilindi.")
    if user_id in pending_payments:
        del pending_payments[user_id]

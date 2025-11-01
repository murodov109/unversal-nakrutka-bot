from db import Database
from telebot import types
from config import CARD_NUMBER

db = Database()

def handle_payment(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💳 Pul kiritish", "💰 Balansim")
    markup.add("⬅️ Asosiy menyuga qaytish")
    bot.send_message(message.chat.id, "💵 To‘lov bo‘limiga xush kelibsiz!", reply_markup=markup)

def handle_payment_menu(bot, message):
    if message.text == "💳 Pul kiritish":
        bot.send_message(message.chat.id, f"💳 To‘lov uchun karta raqami:\n\n{CARD_NUMBER}\n\nTo‘lov qilgach, chekni (rasmni) yuboring.")
        bot.register_next_step_handler(message, lambda msg: confirm_payment(bot, msg))
    elif message.text == "💰 Balansim":
        balance = db.get_balance(message.from_user.id)
        bot.send_message(message.chat.id, f"💰 Sizning balansingiz: {balance} so‘m")
    elif message.text == "⬅️ Asosiy menyuga qaytish":
        from user_panel import main_menu
        main_menu(bot, message)

def confirm_payment(bot, message):
    if not message.photo:
        bot.send_message(message.chat.id, "❌ Rasm yuboring (chek).")
        return

    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    db.add_task("To‘lov", f"Foydalanuvchi {user_id} to‘lov cheki yubordi.")
    bot.send_message(message.chat.id, "✅ To‘lov tekshirishga yuborildi! Tez orada tasdiqlanadi.")

from db import Database
from telebot import types

db = Database()

def handle_order(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📢 Buyurtma berish", "📋 Mening buyurtmalarim")
    markup.add("⬅️ Asosiy menyuga qaytish")
    bot.send_message(message.chat.id, "🛒 Buyurtma bo‘limiga xush kelibsiz!", reply_markup=markup)

def handle_order_menu(bot, message):
    if message.text == "📢 Buyurtma berish":
        bot.send_message(message.chat.id, "📄 Buyurtma nomini kiriting:")
        bot.register_next_step_handler(message, lambda msg: ask_description(bot, msg))
    elif message.text == "📋 Mening buyurtmalarim":
        bot.send_message(message.chat.id, "🗒 Hozircha buyurtmalaringiz yo‘q.")
    elif message.text == "⬅️ Asosiy menyuga qaytish":
        from user_panel import main_menu
        main_menu(bot, message)

def ask_description(bot, message):
    task_name = message.text
    bot.send_message(message.chat.id, "📝 Buyurtma tavsifini yozing:")
    bot.register_next_step_handler(message, lambda msg: save_order(bot, msg, task_name))

def save_order(bot, message, task_name):
    description = message.text
    db.add_task(task_name, description)
    bot.send_message(message.chat.id, f"✅ Buyurtma saqlandi!\n🧾 Nomi: {task_name}\n📃 Tavsif: {description}")

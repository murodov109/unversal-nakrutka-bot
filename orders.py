from telebot import types
from db import load_data, save_data, add_order, get_user_balance, update_user_balance
from config import PRICE_PER_SUB, ADMINS
import time

orders = {}

def order_menu(bot, message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "📦 Nechta obunachi buyurtma qilmoqchisiz?\n\nMasalan: 10")
    bot.register_next_step_handler(message, process_amount, bot)

def process_amount(message, bot):
    chat_id = message.chat.id
    if not message.text.isdigit():
        bot.send_message(chat_id, "❌ Iltimos, faqat raqam kiriting.")
        return order_menu(bot, message)
    orders[chat_id] = {"amount": int(message.text)}
    bot.send_message(chat_id, "🔗 Endi kanal yoki guruh havolasini yuboring:")
    bot.register_next_step_handler(message, process_link, bot)

def process_link(message, bot):
    chat_id = message.chat.id
    link = message.text
    amount = orders[chat_id]["amount"]
    cost = amount * PRICE_PER_SUB
    balance = get_user_balance(chat_id)
    if balance < cost:
        bot.send_message(chat_id, f"❌ Balansingizda yetarli mablag‘ yo‘q.\nKerakli summa: {cost} so‘m\nBalansingiz: {balance} so‘m")
        return
    orders[chat_id]["link"] = link
    orders[chat_id]["cost"] = cost
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"confirm_order_{chat_id}"))
    markup.add(types.InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_order"))
    bot.send_message(chat_id, f"📋 Buyurtmani tasdiqlaysizmi?\n\n🔗 Havola: {link}\n👥 Obunachilar: {amount}\n💰 Narx: {cost} so‘m", reply_markup=markup)

def confirm_order(bot, call):
    chat_id = call.from_user.id
    if chat_id not in orders:
        bot.answer_callback_query(call.id, "❌ Buyurtma topilmadi.")
        return
    data = orders[chat_id]
    balance = get_user_balance(chat_id)
    if balance < data["cost"]:
        bot.answer_callback_query(call.id, "❌ Balansingizda mablag‘ yetarli emas.")
        return
    update_user_balance(chat_id, -data["cost"])
    add_order(chat_id, data["link"], data["amount"], 0)
    del orders[chat_id]
    bot.answer_callback_query(call.id, "✅ Buyurtma qabul qilindi!")
    bot.send_message(chat_id, "🎉 Buyurtmangiz muvaffaqiyatli yaratildi!\nKanalga tez orada joylanadi.")

    text = f"📢 Yangi buyurtma!\n\n🔗 Kanal: {data['link']}\n👥 Obunachilar: {data['amount']}\n💰 Mukofot: {PRICE_PER_SUB} so‘m\n\nBoshlang!"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"💸 Pul ishlash (0/{data['amount']})", callback_data=f"work_{chat_id}_0_{data['amount']}"))
    for admin_id in ADMINS:
        bot.send_message(admin_id, text, reply_markup=markup)

def handle_work(bot, call):
    parts = call.data.split("_")
    user_id = call.from_user.id
    order_owner = int(parts[1])
    done = int(parts[2])
    total = int(parts[3])

    data = load_data()
    user_id_str = str(user_id)
    if "completed_tasks" not in data["users"][user_id_str]:
        data["users"][user_id_str]["completed_tasks"] = []
    task_key = f"{order_owner}_{total}"
    if task_key in data["users"][user_id_str]["completed_tasks"]:
        bot.answer_callback_query(call.id, "❌ Siz bu vazifani allaqachon bajargansiz.")
        return

    data["users"][user_id_str]["balance"] += PRICE_PER_SUB
    data["users"][user_id_str]["completed_tasks"].append(task_key)
    save_data(data)

    new_done = done + 1
    if new_done < total:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"💸 Pul ishlash ({new_done}/{total})", callback_data=f"work_{order_owner}_{new_done}_{total}"))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Buyurtma bajarildi", callback_data="done"))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)

    bot.answer_callback_query(call.id, f"💰 Hisobingizga {PRICE_PER_SUB} so‘m qo‘shildi!")

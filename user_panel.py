import telebot
from telebot import types
import random
from config import BOT_TOKEN, PRICE_PER_SUB, REF_BONUS, BONUS_MIN, BONUS_MAX, CARD_NUMBER, MANDATORY_CHANNELS
from database.db import load_db, save_db, register_user, get_user, add_balance, can_take_bonus, set_bonus_taken, add_referral, add_order, complete_order, add_payment_request, get_required_channels, add_required_channel, remove_required_channel

bot = telebot.TeleBot(BOT_TOKEN)

def ensure_user(user_id, first_name="User"):
    register_user(user_id, first_name)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Foydalanuvchi"
    ensure_user(user_id, first_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 Buyurtma berish", "💰 Hisobim")
    markup.row("🎯 Vazifalar", "💳 Hisobni to‘ldirish")
    markup.row("🎁 Kunlik bonus", "👥 Taklif orqali pul ishlash")
    markup.row("💬 Fikr bildirish")
    bot.send_message(message.chat.id, f"Assalomu alaykum, {first_name}! 👋\nQuyidagi tugmalardan birini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💰 Hisobim")
def my_balance(message):
    uid = message.from_user.id
    ensure_user(uid, message.from_user.first_name or "Foydalanuvchi")
    user = get_user(uid)
    balance = user.get("balance", 0) if user else 0
    refs = len(user.get("referrals", [])) if user else 0
    total_done = len(user.get("completed_tasks", [])) if user else 0
    text = f"🆔 ID: {uid}\n💳 Balans: {balance} so‘m\n👥 Takliflar: {refs}\n✅ Bajarilgan vazifalar: {total_done}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "🛒 Buyurtma berish")
def start_order(message):
    uid = message.from_user.id
    ensure_user(uid, message.from_user.first_name or "Foydalanuvchi")
    msg = bot.send_message(message.chat.id, "📦 Nechta obunachi kerak? (faqat raqam kiriting)")
    bot.register_next_step_handler(msg, order_count_step)

def order_count_step(message):
    try:
        count = int(message.text.strip())
        if count <= 0:
            raise ValueError
    except:
        bot.send_message(message.chat.id, "❌ Iltimos to‘g‘ri raqam kiriting.")
        return
    uid = message.from_user.id
    data = load_db()
    if str(uid) not in data["users"]:
        register_user(uid, message.from_user.first_name or "Foydalanuvchi")
        data = load_db()
    cost = count * PRICE_PER_SUB
    user = data["users"].get(str(uid))
    if user.get("balance", 0) < cost:
        bot.send_message(message.chat.id, f"💸 Hisobingizda yetarli mablag‘ yo‘q. Kerak: {cost} so‘m")
        return
    msg = bot.send_message(message.chat.id, "🔗 Kanal yoki post havolasini yuboring (masalan: https://t.me/kanal/postid yoki @kanal):")
    bot.register_next_step_handler(msg, order_link_step, count, cost)

def order_link_step(message, count, cost):
    link = message.text.strip()
    uid = message.from_user.id
    data = load_db()
    data["users"][str(uid)]["balance"] -= cost
    save_db(data)
    reward = PRICE_PER_SUB
    add_order(link, reward, count)
    data = load_db()
    order_index = len(data["orders"]) - 1
    channel_to_post = None
    channels = get_required_channels()
    if channels:
        channel_to_post = channels[0]
    else:
        if MANDATORY_CHANNELS:
            channel_to_post = MANDATORY_CHANNELS[0]
    inline = types.InlineKeyboardMarkup()
    inline.add(types.InlineKeyboardButton(f"💸 Pul ishlash (0/{count})", callback_data=f"work_{order_index}"))
    post_text = f"🆕 Yangi buyurtma #{order_index}\n🔗 {link}\nHar bir bajaruvchi: {reward} so‘m"
    try:
        if channel_to_post:
            bot.send_message(channel_to_post, post_text, reply_markup=inline)
    except:
        pass
    bot.send_message(message.chat.id, f"✅ Buyurtma qabul qilindi. Jami: {cost} so‘m. Buyurtma ID: {order_index}")

@bot.callback_query_handler(func=lambda c: c.data.startswith("work_"))
def callback_work(call):
    parts = call.data.split("_", 1)
    if len(parts) < 2:
        bot.answer_callback_query(call.id, "Xato.")
        return
    order_idx = int(parts[1])
    data = load_db()
    if order_idx < 0 or order_idx >= len(data["orders"]):
        bot.answer_callback_query(call.id, "Buyurtma topilmadi.")
        return
    order = data["orders"][order_idx]
    uid = call.from_user.id
    if str(uid) == str(order.get("owner")):
        bot.answer_callback_query(call.id, "O‘zingizning buyurtmangizni bajara olmaysiz.")
        return
    if str(order_idx) in data["users"].get(str(uid), {}).get("completed_tasks", []):
        bot.answer_callback_query(call.id, "✅ Siz bu vazifani allaqachon bajargansiz.")
        return
    required = get_required_channels()
    all_joined = True
    for ch in required:
        try:
            status = bot.get_chat_member(ch, uid).status
            if status not in ["member", "administrator", "creator"]:
                all_joined = False
                break
        except:
            all_joined = False
            break
    if not all_joined:
        bot.answer_callback_query(call.id, "🚫 Avval majburiy kanallarga obuna bo‘ling.")
        return
    success = complete_order(uid, order.get("channel"))
    if not success:
        bot.answer_callback_query(call.id, "Siz ushbu vazifani bajargansiz yoki xato.")
        return
    data = load_db()
    data["users"].setdefault(str(uid), {}).setdefault("completed_tasks", []).append(str(order_idx))
    save_db(data)
    done = order.get("completed", 0)
    total = order.get("max_count", 0)
    if done >= total:
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None)
            bot.send_message(call.message.chat.id, f"✅ Buyurtma #{order_idx} muvaffaqiyatli bajarildi!")
        except:
            pass
    else:
        try:
            new_markup = types.InlineKeyboardMarkup()
            new_markup.add(types.InlineKeyboardButton(f"💸 Pul ishlash ({done}/{total})", callback_data=f"work_{order_idx}"))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=new_markup)
        except:
            pass
    bot.answer_callback_query(call.id, "💰 Vazifa bajarildi, balansga qo‘shildi!")

@bot.message_handler(func=lambda m: m.text == "🧾 Vazifalar" or m.text == "🎯 Vazifalar")
def list_tasks(message):
    data = load_db()
    orders = data.get("orders", [])
    if not orders:
        bot.send_message(message.chat.id, "📭 Hozircha vazifalar yo‘q.")
        return
    text = "🎯 Aktiv vazifalar:\n\n"
    for idx, o in enumerate(orders):
        text += f"#{idx} | {o.get('channel')} | {o.get('reward')} so‘m | {o.get('completed')}/{o.get('max_count')}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "💳 Hisobni to‘ldirish")
def start_payment(message):
    uid = message.from_user.id
    ensure_user(uid, message.from_user.first_name or "Foydalanuvchi")
    msg = bot.send_message(message.chat.id, "💸 To‘ldirmoqchi bo‘lgan summangizni kiriting (so‘m):")
    bot.register_next_step_handler(msg, payment_amount_step)

def payment_amount_step(message):
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            raise ValueError
    except:
        bot.send_message(message.chat.id, "❌ Iltimos to‘g‘ri summa kiriting.")
        return
    uid = message.from_user.id
    bot.send_message(message.chat.id, f"💳 Iltimos quyidagi karta raqamiga to‘lov qiling:\n\n{CARD_NUMBER}\n\nTo‘lovdan so‘ng chek yoki skrinshot yuboring.")
    msg = bot.send_message(message.chat.id, "📎 Chekni yuboring (rasm yoki fayl):")
    bot.register_next_step_handler(msg, payment_receipt_step, amount)

def payment_receipt_step(message, amount):
    uid = message.from_user.id
    file_id = None
    if message.content_type == "photo":
        file_id = message.photo[-1].file_id
    elif message.content_type == "document":
        file_id = message.document.file_id
    else:
        bot.send_message(message.chat.id, "❌ Iltimos faqat rasm yoki fayl yuboring.")
        return
    add_payment_request(uid, amount, file_id)
    bot.send_message(message.chat.id, "📨 Ariza yuborildi. Admin tasdiqlashini kuting.")
    admins = load_db().get("users", {})
    for uid_key, info in admins.items():
        if info.get("is_admin"):
            try:
                bot.send_photo(int(uid_key), file_id, caption=f"📩 Yangi to‘lov arizasi\nFoydalanuvchi ID: {message.from_user.id}\nSumma: {amount} so‘m")
            except:
                pass

@bot.message_handler(func=lambda m: m.text == "👥 Taklif orqali pul ishlash" or m.text == "🤝 Pul ishlash")
def referral_info(message):
    me = bot.get_me()
    ref_link = f"https://t.me/{me.username}?start={message.from_user.id}"
    bot.send_message(message.chat.id, f"🤝 Sizning referal havolangiz:\n{ref_link}\n1-daraja: {REF_BONUS} so‘m\n2-daraja: 100 so‘m")

@bot.message_handler(func=lambda m: m.text == "🎁 Kunlik bonus")
def daily_bonus(message):
    uid = message.from_user.id
    ensure_user(uid, message.from_user.first_name or "Foydalanuvchi")
    if not can_take_bonus(uid):
        bot.send_message(message.chat.id, "❌ Siz bugun allaqachon bonus olgansiz. Ertaga urinib ko‘ring.")
        return
    amount = random.randint(BONUS_MIN, BONUS_MAX)
    add_balance(uid, amount)
    set_bonus_taken(uid)
    bot.send_message(message.chat.id, f"🎉 Sizga {amount} so‘m kunlik bonus berildi!")

@bot.message_handler(func=lambda m: m.text == "💬 Fikr bildirish")
def feedback_start(message):
    msg = bot.send_message(message.chat.id, "✉️ Fikr yoki muammoni yozing. Adminlarga yuboraman.")
    bot.register_next_step_handler(msg, feedback_send)

def feedback_send(message):
    text = message.text or ""
    uid = message.from_user.id
    admins = load_db().get("users", {})
    for uid_key, info in admins.items():
        if info.get("is_admin"):
            try:
                bot.send_message(int(uid_key), f"💬 Yangi fikr\nFrom: {uid}\n\n{text}")
            except:
                pass
    bot.send_message(message.chat.id, "📨 Fikringiz adminlarga yuborildi. Rahmat!")

bot.infinity_polling(skip_pending=True)

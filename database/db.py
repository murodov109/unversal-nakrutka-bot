import json
import os
from config import DB_PATH

def load_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"users": {}, "orders": [], "channels": []}, f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def add_user(user_id):
    data = load_db()
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {
            "balance": 0,
            "referrals": [],
            "joined": False,
            "bonus_taken": False
        }
        save_db(data)

def get_balance(user_id):
    data = load_db()
    return data["users"].get(str(user_id), {}).get("balance", 0)

def update_balance(user_id, amount):
    data = load_db()
    uid = str(user_id)
    if uid not in data["users"]:
        add_user(user_id)
    data["users"][uid]["balance"] = data["users"][uid].get("balance", 0) + amount
    save_db(data)

def add_referral(owner_id, ref_id):
    data = load_db()
    owner = str(owner_id)
    if owner not in data["users"]:
        add_user(owner_id)
    if ref_id not in data["users"][owner]["referrals"]:
        data["users"][owner]["referrals"].append(ref_id)
        save_db(data)

def add_order(user_id, channel, amount, target):
    data = load_db()
    data["orders"].append({
        "user_id": user_id,
        "channel": channel,
        "amount": amount,
        "target": target,
        "done": 0
    })
    save_db(data)

def get_orders():
    data = load_db()
    return data["orders"]

def update_order_progress(channel, done):
    data = load_db()
    for order in data["orders"]:
        if order["channel"] == channel:
            order["done"] = done
    save_db(data)

def get_channels():
    data = load_db()
    return data["channels"]

def set_channels(channels):
    data = load_db()
    data["channels"] = channels
    save_db(data)

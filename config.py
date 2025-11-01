import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8435705646:AAEJULzHr7N2Z-lleYsoQKf36yVnHxd0iXU")
BOT_USERNAME = os.getenv("BOT_USERNAME", "@jonli_obunachipro_bot")
ADMINS = [7617397626]
CARD_NUMBER = "5440810305608647"

PRICE_PER_SUB = 0.15
REF_BONUS = 1.0
BONUS_MIN = 0.5
BONUS_MAX = 2.0

MANDATORY_CHANNELS = [
    "https://t.me/jonli_obunachipro",
    "https://t.me/test_kanal_1"
]

DB_NAME = "database.db"
ON_RENDER = os.getenv("ON_RENDER", "False").lower() == "true"
TOKEN = BOT_TOKEN

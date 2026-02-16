import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
OWNER_ID = int(os.environ.get("OWNER_ID", 8587740350))  # Your Telegram User ID
ADMINS = [8587740350] + [
    int(admin) for admin in os.environ.get("ADMINS", "").split(",") if admin
]

DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "SaveRestricted2")

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

ERROR_MESSAGE = os.environ.get("ERROR_MESSAGE", "True").lower() == "true"

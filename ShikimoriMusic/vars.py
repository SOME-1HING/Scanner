
import os

que = {}
admins = {}

BG_IMG = os.environ.get("BG_IMG", "https://i.imgur.com/W3Jyec6.jpg")
START_PIC = BG_IMG
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

SESSION_STRING = os.environ.get("SESSION_STRING", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
API_ID = int(os.environ.get("API_ID", None))
API_HASH = os.environ.get("API_HASH", None)
OWNER_ID = int(os.environ.get("OWNER_ID", None))
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
UPDATE = os.environ.get("UPDATE", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
DURATION_LIMIT = int(os.environ.get("DURATION_LIMIT", "600"))
CMD_MUSIC = list(os.environ.get("CMD_MUSIC", "/ !").split())
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", None)


SUDO_USERS = (OWNER_ID, 5499316076)

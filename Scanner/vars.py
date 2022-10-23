
import os

que = {}
admins = {}

SESSION_STRING = os.environ.get("SESSION_STRING", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
API_ID = int(os.environ.get("API_ID", None))
API_HASH = os.environ.get("API_HASH", None)
OWNER_ID = int(os.environ.get("OWNER_ID", None))
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
UPDATE = os.environ.get("UPDATE", None)
CMD_OP = list(os.environ.get("CMD_OP", "/ . ? !").split())
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
LOG_CHANNEL_ID = os.environ.get("LOG_CHANNEL_ID", None)

SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
SUDO_USERS.append(OWNER_ID)
GBAN_CHATS = set(int(x) for x in os.environ.get("GBAN_CHATS", "").split())
import logging
import time
from ShikimoriMusic.vars import API_HASH, API_ID, BOT_TOKEN, SESSION_STRING

from pytgcalls import PyTgCalls
from pyrogram import Client

starttime = time.time()

# enable logging
FORMAT = "[ShikimoriMusic] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("ShikimoriMusic_logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)

LOGGER = logging.getLogger('[ShikimoriMusic]')
LOGGER.info("ShikimoriMusic is starting. | Built by SOME1HING. | Licensed under GPLv3.")
LOGGER.info("Handled by: github.com/SOME-1HING (t.me/SOME1HING)")


calls = Client(SESSION_STRING, API_ID, API_HASH)
pytgcalls = PyTgCalls(calls)
pbot = Client("ShikimoriMusic", API_ID, API_HASH, bot_token=BOT_TOKEN)
ubot = Client(SESSION_STRING, API_ID, API_HASH)


pbot.start()
ubot.start()

bot = pbot.get_me()
BOT_ID = bot.id
if bot.last_name:
    BOT_NAME = bot.first_name + " " + bot.last_name
else:
    BOT_NAME = bot.first_name
BOT_USERNAME = bot.username

ub = ubot.get_me()
ASS_ID = ub.id
if ub.last_name:
    ASS_NAME = ub.first_name + " " + ub.last_name
else:
    ASS_NAME = ub.first_name
ASS_USERNAME = ub.username
import logging
import asyncio
import time
from ShikimoriMusic.vars import API_HASH, API_ID, BOT_TOKEN, SESSION_STRING

from pytgcalls import PyTgCalls
from pyrogram import Client
from telegram.error import BadRequest, Forbidden
from telegram.ext import Application

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

# PTB Client
async def post_init(application: Application):
    try:
        await application.bot.sendMessage(-1001717154437, "👋 Hi, i'm alive.")
    except Forbidden:
        LOGGER.warning(
            "Bot isn't able to send message to support_chat, gos and check!",
        )
    except BadRequest as e:
        LOGGER.warning(e.message)


application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
asyncio.get_event_loop().run_until_complete(application.bot.initialize())

print("[INFO]: PTB CLIENT INITIALIZED")
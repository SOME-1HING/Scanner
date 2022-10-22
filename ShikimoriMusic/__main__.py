import asyncio
import requests

from pyrogram import Client
from pytgcalls import idle

from ShikimoriMusic import LOGGER, pbot, ubot
from ShikimoriMusic.vars import API_ID, API_HASH, BOT_TOKEN, BG_IMG

response = requests.get(BG_IMG)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)

async def load_start():
    LOGGER.info("[INFO]: STARTED")
    await pbot.send_message(
        -1001717154437, "**Pyrogram Client Started Successfully !!**"
    )
    LOGGER.info("[INFO]: PYROGRAM STARTED")
    await ubot.send_message(
        -1001717154437, "**Assistant Started Successfully !!**"
    )
    

loop = asyncio.get_event_loop_policy().get_event_loop()
loop.run_until_complete(load_start())

Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "ShikimoriMusic.plugins"},
).start()

idle()
loop.close()

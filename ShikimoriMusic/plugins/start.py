from ShikimoriMusic.mongo.chats import add_served_chat, is_served_chat
from ShikimoriMusic.mongo.users import add_served_user, is_served_user
from ShikimoriMusic.plugins.stats import get_readable_time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import time
from datetime import datetime

from ShikimoriMusic.setup.filters import command
from ShikimoriMusic.vars import SUPPORT_CHAT
from ShikimoriMusic import BOT_USERNAME, starttime

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    if not is_served_user(message.from_user.id):
        add_served_user(message.from_user.id)
    await message.reply_text(
        f"""ᴡᴇʟᴄᴏᴍᴇ : {message.from_user.mention()}

ɪ ᴀᴍ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ᴀɴᴅ ᴜsᴇғᴜʟ ғᴇᴀᴛᴜʀᴇs.

ᴜsᴇ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ !!""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🗂 ᴄᴏᴍᴍᴀɴᴅs", callback_data="cmds"),
                    InlineKeyboardButton(
                        "🆘 ʜᴇʟᴘ", url=f"https://t.me/{SUPPORT_CHAT}")
                ],
                [
                    InlineKeyboardButton(
                        "✚ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
           ]
        ),
    )

@Client.on_message(command("start") & ~filters.private & ~filters.edited)
async def start_grp(client: Client, message: Message):
    if not is_served_user(message.from_user.id):
        add_served_user(message.from_user.id)
    if not is_served_chat(message.chat.id):
        try:
            add_served_chat(message.chat.id)
            pass
        except:
            pass
    botuptime = get_readable_time((time.time() - starttime))
    await message.reply_text(
        f"Hey {message.from_user.mention()}, I'm here for you at {message.chat.title} since : `{botuptime}`")
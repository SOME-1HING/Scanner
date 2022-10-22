from ShikimoriMusic.mongo.chats import add_served_chat, is_served_chat
from ShikimoriMusic.mongo.users import add_served_user, is_served_user
from ShikimoriMusic.plugins.stats import get_readable_time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import time
from datetime import datetime

from ShikimoriMusic.setup.filters import command
from ShikimoriMusic.vars import OWNER_ID, SUDO_USERS, SUPPORT_CHAT
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

@Client.on_message(command(["ping"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("ᴘɪɴɢ..... 👀")
    delta_ping = time() - start
    await m_reply.edit_text("ᴘᴏɴɢ.... 🥵\n" f"`{delta_ping * 1000:.3f} ᴍx`")

@Client.on_message(filters.new_chat_members)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if not is_served_chat(chat_id):
        try:
            add_served_chat(chat_id)
            pass
        except:
            pass
    for member in message.new_chat_members:
        if member.id ==OWNER_ID:
            return await message.reply_video(
                video="https://telegra.ph/file/e6fcbd9f756006c2329f6.mp4",
                caption="ʜᴇʏʏ ғᴇʟʟᴀs ! ʟᴏᴏᴋ ᴡʜᴏ ᴀʀʀɪᴠᴇᴅ.... ɪᴛs ᴍʏ ᴏᴡɴᴇʀ ᴜᴡᴜ~",
            )
        if member.id in SUDO_USERS:
            return await message.reply_animation(
                "https://telegra.ph/file/382c47440fa726549b49d.mp4",
                caption="Behold A SUDO User has just joined the chat.",
            )
        return
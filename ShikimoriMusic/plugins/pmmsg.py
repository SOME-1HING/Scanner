# Copyright (©️) @KIRITO_1240
# By : KIRITO

from ShikimoriMusic.mongo.users import add_served_user
from pyrogram import Client
from ShikimoriMusic.calls import client as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User

from ShikimoriMusic.vars import SUPPORT_CHAT

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  add_served_user(message.from_user.id)
  await USER.send_message(message.chat.id,f"Hey 👋 I am the assistant of Shikimori Music bot, didn't have a time to talk with you 🙂 kindly join @{SUPPORT_CHAT} for getting Support.")
  return

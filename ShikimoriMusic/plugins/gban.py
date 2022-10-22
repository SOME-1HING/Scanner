from functools import wraps
import html
import time
from datetime import datetime
from io import BytesIO

from telegram import ChatMemberAdministrator, Update, Chat, ChatMember
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden, TelegramError
from telegram.ext import CallbackContext, ContextTypes
from pyrogram.types import Message
from telegram.helpers import mention_html
from pyrogram import Client
from ShikimoriMusic import ASS_ID, BOT_ID, pbot, ubot, LOGGER
from ShikimoriMusic.plugins.extraction import extract_user_and_text, extract_user
from ShikimoriMusic.vars import OWNER_ID, SUPPORT_CHAT, SUDO_USERS, GBAN_CHATS
from ShikimoriMusic.setup.filters import command
from ShikimoriMusic.mongo import global_bans_db as db

def extract_gban(message):
    hmmm = message.split("-id")[1]
    hmm = hmmm.split("-r")  
    id = int(hmm[0].split()[0].strip())
    reason = hmm[1].split("-p")[0].strip()
    proof = hmm[1].split("-p")[1].strip()
    return id, reason, proof

def is_sudo_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return user_id in SUDO_USERS

def sudo_plus(func):
    @wraps(func)
    async def is_sudo_plus_func(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        context.bot
        user = update.effective_user
        chat = update.effective_chat

        if user and is_sudo_plus(chat, user.id):
            return await func(update, context, *args, **kwargs)
        elif not user:
            pass
        elif " " not in update.effective_message.text:
            try:
                await update.effective_message.delete()
            except:
                pass
        else:
            await update.effective_message.reply_text(
                "Who the hell are you to say me what to do?",
            )

    return is_sudo_plus_func

@sudo_plus
@Client.on_message(command("scan"))
async def scan(_, message: Message):
    try:
        user_id, reason, proof = extract_gban(message.text)
    except:
        await message.reply_text("/scan -id (id) -r (reason)  -p (proof link)")
        return
    if int(user_id) in SUDO_USERS:
        await message.reply_text(
            "That user is part of the Association\nI can't act against our own.",
        )
        return
    
    if user_id == BOT_ID or user_id == ASS_ID:
        await message.reply_text("You uhh...want me to punch myself?")
        return
    if user_id in [777000, 1087968824]:
        await message.reply_text("Fool! You can't attack Telegram's native tech!")
        return

    db.gban_user(user_id, reason)
    for chat_id in GBAN_CHATS:
        await ubot.send_message(
            chat_id,
            f"/gban {user_id} {reason}. Scanned by {message.from_user.id}"
        )

@sudo_plus
@Client.on_message(command("revert"))
async def revert(_, message: Message):
    try:
        user_id, reason, proof = extract_gban(message.text)
    except:
        try:
            hmmm = message.text.split("-id")[1]
            user_id = int(hmmm.strip())
        except:
            LOGGER.info(message.text)
            await message.reply_text("/revert -id (id)")
            return
    if int(user_id) in SUDO_USERS:
        await message.reply_text(
            "That user is part of the Association\nI can't act against our own.",
        )
        return
    
    if user_id == BOT_ID or user_id == ASS_ID:
        await message.reply_text("You uhh...want me to punch myself?")
        return
    if user_id in [777000, 1087968824]:
        await message.reply_text("Fool! You can't attack Telegram's native tech!")
        return
    try:
        reason = f"{reason} + {proof}"
    except:
        reason = None

    db.ungban_user(user_id)
    for chat_id in GBAN_CHATS:
        await ubot.send_message(
            chat_id,
            f"/ungban {user_id} {reason}. Reverted by {message.from_user.id}" if reason else f"/ungban {user_id}. Reverted by {message.from_user.id}" 
        )
    
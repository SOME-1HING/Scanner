from pyrogram.types import Message
from pyrogram import Client

from ShikimoriMusic import ASS_ID, BOT_ID, ubot, LOGGER
from ShikimoriMusic.vars import SUDO_USERS, GBAN_CHATS
from ShikimoriMusic.setup.filters import command
from ShikimoriMusic.mongo import global_bans_db as db

def extract_gban(message):
    hmmm = message.split("-id")[1]
    hmm = hmmm.split("-r")  
    id = int(hmm[0].split()[0].strip())
    reason = hmm[1].split("-p")[0].strip()
    proof = hmm[1].split("-p")[1].strip()
    return id, reason, proof

@Client.on_message(command("scan"))
async def scan(_, message: Message):
    if message.from_user.id not in SUDO_USERS:
        await message.reply_text(
            "You need to be part of the Association to scan a user.",
        )
        return
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

@Client.on_message(command("revert"))
async def revert(_, message: Message):
    if message.from_user.id not in SUDO_USERS:
        await message.reply_text(
            "You need to be part of the Association to scan a user.",
        )
        return
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

    db.ungban_user(user_id)
    for chat_id in GBAN_CHATS:
        await ubot.send_message(
            chat_id,
            f"/ungban {user_id}"
        )
    
from io import BytesIO

from pyrogram.types import Message
from pyrogram import Client

from Scanner import ASS_ID, BOT_ID, pbot, ubot
from Scanner.vars import LOG_CHANNEL_ID, SUDO_USERS, GBAN_CHATS
from Scanner.utils.filters import command
from Scanner.db import global_bans_db as db

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
    except ValueError:
        await message.reply_text("id must be integer.")
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

    for chat_id in GBAN_CHATS:
        await ubot.send_message(
            chat_id,
            f"/gban {user_id} {reason} Proof: {proof}. Scanned by {message.from_user.id}"
        )
    db.gban_user(user_id, reason)
    await message.reply_text(
        f"""
# SCANNED
User ID: {user_id}
Reason: {reason}
Proof: {proof}

Scanned By: {message.from_user.id}
"""
    )
    await pbot.send_message(
        LOG_CHANNEL_ID,
        f"""
# SCANNED
User ID: {user_id}
Reason: {reason}
Proof: {proof}

Scanned By: {message.from_user.id}
"""
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
        except ValueError:
            await message.reply_text("id must be integer.")
        except:
            await message.reply_text("/revert -id (id)")
            return
    if not db.is_user_gbanned(user_id):
        await message.reply_text(f"User ID: {user_id} is not scanned.")
        return
    for chat_id in GBAN_CHATS:
        await ubot.send_message(
            chat_id,
            f"/ungban {user_id}"
        )
    db.ungban_user(user_id)
    await message.reply_text(
        f"""
# REVERTED
User ID: {user_id}

Reverted By: {message.from_user.id}
"""
    )
    await pbot.send_message(
        LOG_CHANNEL_ID,
        f"""
# REVERTED
User ID: {user_id}

Reverted By: {message.from_user.id}
"""
    )
    
@Client.on_message(command("scanlist"))
async def scanlist(_, message: Message):
    banned_users = db.get_gban_list()
    
    if not banned_users:
        await message.reply_text(
            "There aren't any gbanned users! You're kinder than I expected...",
        )
        return

    banfile = "Screw these guys.\n"
    for user in banned_users:
        banfile += f"[x] {user['user_id']}\n"
        if user["reason"]:
            banfile += f"Reason: {user['reason']}\n"

    with BytesIO(str.encode(banfile)) as output:
        output.name = "gbanlist.txt"
        await message.reply_document(
            document=output,
            file_name="gbanlist.txt",
            caption="Here is the list of currently gbanned users.",
        )

from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
from telethon import events
from Scanner import tbot

@tbot.on(events.NewMessage(pattern="^/gscan ?(.*)"))
async def gscan(hmm):
    if not hmm.is_group:
        return
    if hmm.is_group:
        if hmm.sender_id not in SUDO_USERS:
            return
    res = hmm.pattern_match.group(1)
    if not res:
       await hmm.reply('Provide Some Reason')
       return
    else:
       reason = f"{res}. Gscaned by {hmm.sender_id}"
    async for user in tbot.iter_participants(hmm.chat_id):
        if not user.deleted and user.id not in SUDO_USERS and user.id != BOT_ID and user.id != ASS_ID and user.id not in [777000, 1087968824]:
            try:
                for chat_id in GBAN_CHATS:
                    await ubot.send_message(
                        chat_id,
                        f"/gban {user.id} {reason}"
                    )
                db.gban_user(user.id, reason)
                await hmm.reply(
        f"""
# GSCANNED
User ID: {user.id}
Reason: {reason}

GScanned By: {hmm.sender_id}
"""
    )
                await pbot.send_message(
                    LOG_CHANNEL_ID,
        f"""
# GSCANNED
User ID: {user.id}
Reason: {reason}

GScanned By: {hmm.sender_id}
"""
    )
            except:
                pass
            
@tbot.on(events.NewMessage(pattern="^/grevert ?(.*)"))
async def grevert(hmm):
    if not hmm.is_group:
        return
    if hmm.is_group:
        if hmm.sender_id not in SUDO_USERS:
            return
    async for user in tbot.iter_participants(hmm.chat_id):
        if not user.deleted and user.id not in [777000, 1087968824]:
            try:
                for chat_id in GBAN_CHATS:
                    await ubot.send_message(
                        chat_id,
                        f"/ungban {user.id}"
                    )
                db.ungban_user(user.id)
                await hmm.reply(
        f"""
# GREVERTED
User ID: {user.id}

GReverted By: {hmm.sender_id}
"""
    )
                await pbot.send_message(
                    LOG_CHANNEL_ID,
        f"""
# GREVERTED
User ID: {user.id}

GReverted By: {hmm.sender_id}
"""
    )
            except:
                pass
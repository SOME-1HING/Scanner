from io import BytesIO
import json

from pyrogram.types import Message, ChatMember
from pyrogram import Client, filters, enums

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

@ubot.on_message(command("scan"))
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
        return
    except:
        await message.reply_text("Format: `/scan -id (id) -r (reason)  -p (proof link)`")
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
    
    if db.is_user_gbanned(user_id):
        await message.reply_text(f"""
User ID: {user_id} is already scanned.
Reason: {db.get_gbanned_user(user_id)["reason"]}

Scanned By: {db.get_gbanned_user(user_id)["scanner"]}
""")
        return

    for chat_id in GBAN_CHATS:
        await ubot.send_message(
            chat_id,
            f"/gban {user_id} {reason} Proof: {proof}. Scanned by {message.from_user.id}"
        )
    db.gban_user(user_id, message.from_user.id, f"{reason} Proof: {proof}")
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

@ubot.on_message(command("revert"))
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
            await message.reply_text("Format: `/revert -id (id)`")
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

@ubot.on_message(command("gscan") & filters.group)
async def gscan(_, message: Message):
    if message.from_user.id not in SUDO_USERS:
        await message.reply_text(
            "You need to be part of the Association to scan a user.",
        )
        return
    
    res = message.text
    try:
        Test = message.text.split(" ")
        res = " ".join(Test[1:])
        reason = f"{res}. Gscaned by {message.from_user.id}"
    except IndexError:
       await message.reply_text('Provide Some Reason')
       return
        
    scanned = []
    async for userObject in ubot.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        myobject = json.loads(f"{userObject}")
        user = myobject["user"]
        if not user["is_deleted"]  and user['id'] not in SUDO_USERS and user['id'] != BOT_ID and user["id"] != ASS_ID and user['id'] not in [777000, 1087968824] and not user['is_bot']:
            try:
                for chat_id in GBAN_CHATS:
                    await ubot.send_message(
                        chat_id,
                        f"/gban {user['id']} {reason}"
                    )
                db.gban_user(user['id'], message.from_user.id, reason)
                scanned.append(user['id'])
                
            except Exception as e:
                await message.reply_text(f"Error Ocurred: {e}")
                
    if scanned:
        text = "# GSCANNED LIST\n"
        for user_id in scanned:
            text += f"• {user_id}"
        text += f'GScanned By: {message.from_user.id}'
        await message.reply_text(text)
        await pbot.send_message(LOG_CHANNEL_ID, text)

@ubot.on_message(command("grevert") & filters.group)
async def grevert(_, message: Message):
    if message.from_user.id not in SUDO_USERS:
        await message.reply_text(
            "You need to be part of the Association to scan a user.",
        )
        return
    reverted = []
    async for userObject in ubot.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        myobject = json.loads(f"{userObject}")
        user = myobject["user"]
        if not user["is_deleted"]  and user['id'] not in SUDO_USERS and user['id'] != BOT_ID and user["id"] != ASS_ID and user['id'] not in [777000, 1087968824] and not user['is_bot']:
            if db.is_user_gbanned(user['id']):
                try:
                    for chat_id in GBAN_CHATS:
                        
                        await ubot.send_message(
                            chat_id,
                            f"/ungban {user['id']}"
                        )
                    db.ungban_user(user['id'])
                    reverted.append(user['id'])
                except:
                    pass
    if reverted:
        text = "# GREVERT LIST\n"
        for user_id in reverted:
            text += f"• {user_id}"
        text += f'GRevert By: {message.from_user.id}'
        await message.reply_text(text)
        await pbot.send_message(LOG_CHANNEL_ID, text)
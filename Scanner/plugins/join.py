import asyncio
import json

from pyrogram import filters
from pyrogram.errors import UserAlreadyParticipant, FloodWait

from Scanner import ASS_USERNAME, pbot, ubot as USER
from Scanner.utils.decorators import sudo_users_only, errors
from Scanner.utils.administrator import adminsOnly
from Scanner.utils.filters import command
from Scanner.vars import GBAN_CHATS, LOG_CHANNEL_ID, SUDO_USERS

@pbot.on_message(
    command(["userbotjoin", "botjoin", "join"]) & ~filters.private & ~filters.bot
)
@errors
async def joinchat(client, message):
    if "@" in message.text:
        query = message.text
        stopwords = ["/userbotjoin @", "/botjoin @", "/join @"]
        querywords = query.split()
        resultwords  = [word for word in querywords if word.lower() not in stopwords]
        username = ''.join(resultwords[0])
    else:
        await message.reply_text("Format: /join @username")
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = f"{ASS_USERNAME}"

    try:
        message.reply_text(f"https://t.me/{username}")
        await USER.join_chat(f"https://t.me/{username}")
    except UserAlreadyParticipant:
        await message.reply_text(
            f"🔴 **{user.first_name} already join this group !!**",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"❌ **Assistant ({user.first_name}) can't join your group due to many join requests for userbot!**\n‼️ Make sure the user is not banned in the group."
            f"\n\n» `Manually add the {user.first_name} to your group`",
        )
        return
    
@pbot.on_message(
    command(["joinhere"]) & ~filters.private & ~filters.bot
)
@errors
async def addchannel(client, message):
    try:
        invite_link = await message.chat.export_invite_link()
        if "+" in invite_link:
            kontol = (invite_link.replace("+", "")).split("t.me/")[1]
            link_bokep = f"https://t.me/joinchat/{kontol}"
    except:
        await message.reply_text(
            "**Add me admin first**",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = f"{ASS_USERNAME}"

    try:
        await USER.join_chat(link_bokep)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"🔴 **{user.first_name} already join this group !!**",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"❌ **Assistant ({user.first_name}) can't join your group due to many join requests for userbot!**\n‼️ Make sure the user is not banned in the group."
            f"\n\n» `Manually add the {user.first_name} to your group`",
        )
        return

@USER.on_message(filters.group & command(["userbotleave", "odaleave", "odaleft"]))
async def rem(USER, message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    try:
        await USER.send_message(
            message.chat.id,
            "✅ ᴜsᴇʀʙᴏᴛ ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ....",
        )
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "❌ **Assistant can't leave your group! probably waiting for floodwaits**\n\n» Manually remove me from your group</b>"
        )

        return


@pbot.on_message(command(["userbotleaveall", "leaveall"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        await message.reply_text(
            "You need to be part of the Association to scan a user.",
        )
        return
    left = 0
    sleep_time = 0.1
    lol = await message.reply("**Assistant leaving all groups**\n\n`Processing...`")
    async for userObject in USER.get_dialogs():
        dialog = json.loads(f"{userObject}")
        try:
            if dialog['chat']['id'] == GBAN_CHATS or dialog['chat']['id'] == LOG_CHANNEL_ID:
                continue
            await USER.leave_chat(dialog['chat']['id'])
            await asyncio.sleep(sleep_time)
            left += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await lol.edit(f"🏃‍♂️ `Assistant leaving...`\n\n» **Left:** {left} chats.")

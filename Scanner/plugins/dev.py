from Scanner import pbot
from Scanner.vars import OWNER_ID, SUDO_USERS
from pyrogram import Client
from Scanner.utils.filters import command
from pyrogram.types import Message

@Client.on_message(command("leave"))
async def leave(_, message: Message):
    if message.from_user.id in SUDO_USERS:
        if len(message.command) < 2:
            return await message.reply_text("**Usage:**\n/leave [CHAT ID]")
        chat_id = int(message.text.strip().split()[1])
        if chat_id:
            try:
                await pbot.leave_chat(chat_id)
            except:
                await message.reply_text(
                    "Beep boop, I could not leave that group(dunno why tho).",
                )
                return
        else:
            await message.reply_text("Send a valid chat ID")
    else:
        await message.reply_text("This is SUDO restricted command.")

@Client.on_message(command("logs"))
async def logs(_, message: Message):
    if message.from_user.id in SUDO_USERS:
        chat = message.chat
        user = message.from_user
        with open("Scanner_logs.txt", "rb") as f:
            await pbot.send_document(document=f, chat_id=user.id)
        if chat.type != "private":
            await message.reply_text("`Logs sent. Check your pm.`")
    
    else:
        await message.reply_text("This is SUDO restricted command.")

@Client.on_message(command(["sudos", "sudolist"]))
async def sudolist(_, message: Message):
    m = await message.reply_text(
        "<code>Gathering intel..</code>", parse_mode="html"
    )
    img = "https://telegra.ph/file/ee64f19caa9cee3cde865.mp4"
    true_dev = list(set(SUDO_USERS) - {OWNER_ID})
    reply = "<b>Sudo Users:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = await pbot.get_users(user_id)
            user = (
                user.first_name if not user.mention else user.mention
            )
        except:
            user = user_id
        reply += f"• {user}\n"
    await m.delete()
    await message.reply_animation(img, caption=reply, parse_mode="html")
from ShikimoriMusic.mongo.chats import get_served_chats
from ShikimoriMusic.mongo.users import get_served_users
from pyrogram import filters
from pyrogram.errors import FloodWait
import asyncio
from ShikimoriMusic import pbot, ubot
from ShikimoriMusic.vars import SUDO_USERS

@pbot.on_message(filters.command("broadcast"))
async def braodcast_message(_, message):
    if message.from_user.id in SUDO_USERS:
        if message.reply_to_message:
            x = message.reply_to_message.message_id
            y = message.chat.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(_["broad_5"])
            query = message.text.split(None, 1)[1]
            if "-pin" in query:
                query = query.replace("-pin", "")
            if "-nobot" in query:
                query = query.replace("-nobot", "")
            if "-pinloud" in query:
                query = query.replace("-pinloud", "")
            if "-assistant" in query:
                query = query.replace("-assistant", "")
            if "-user" in query:
                query = query.replace("-user", "")
            if query == "":
                return await message.reply_text(_["broad_6"])

        if "-nobot" not in message.text:
            sent = 0
            pin = 0
            chats = []
            schats = get_served_chats()
            for chat in schats:
                chats.append(int(chat["chat_id"]))
            for i in chats:
                try:
                    m = (
                        await pbot.forward_messages(i, y, x)
                        if message.reply_to_message
                        else await pbot.send_message(i, text=query)
                    )
                    if "-pin" in message.text:
                        try:
                            await m.pin(disable_notification=True)
                            pin += 1
                        except Exception:
                            continue
                    elif "-pinloud" in message.text:
                        try:
                            await m.pin(disable_notification=False)
                            pin += 1
                        except Exception:
                            continue
                    sent += 1
                except FloodWait as e:
                    flood_time = int(e.x)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception:
                    continue
            try:
                await message.reply_text(_["broad_1"].format(sent, pin))
            except:
                pass

        if "-user" in message.text:
            susr = 0
            served_users = []
            susers = get_served_users()
            for user in susers:
                served_users.append(int(user["user_id"]))
            for i in served_users:
                try:
                    m = (
                        await pbot.forward_messages(i, y, x)
                        if message.reply_to_message
                        else await pbot.send_message(i, text=query)
                    )
                    susr += 1
                except FloodWait as e:
                    flood_time = int(e.x)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception:
                    pass
            try:
                await message.reply_text(_["broad_7"].format(susr))
            except:
                pass

        if "-assistant" in message.text:
            sent = 0
            async for dialog in ubot.iter_dialogs():
                try:
                    await ubot.forward_messages(
                        dialog.chat.id, y, x
                    ) if message.reply_to_message else await ubot.send_message(
                        dialog.chat.id, text=query
                    )
                    sent += 1
                except FloodWait as e:
                    flood_time = int(e.x)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception as e:
                    print(e)
                    continue
        try:
            await message.reply_text(f"{sent}")
        except:
            pass
    else:
        await message.reply_text("This is SUDO restricted command.")
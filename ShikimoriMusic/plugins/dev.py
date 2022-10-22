import os
import asyncio
import math

import heroku3
import requests

from ShikimoriMusic import pbot
from ShikimoriMusic.vars import OWNER_ID, SUDO_USERS
from pyrogram import Client
from ShikimoriMusic.vars import HEROKU_APP_NAME, HEROKU_API_KEY
from ShikimoriMusic.setup.filters import command
from pyrogram.types import Message

heroku_api = "https://api.heroku.com"
Heroku = heroku3.from_key(HEROKU_API_KEY)

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

@Client.on_message(command("usage"))
async def dyno_usage(_, message: Message):
    if message.from_user.id in SUDO_USERS:
        die = await message.reply_text("`Processing...`")
        useragent = (
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/80.0.3987.149 Mobile Safari/537.36"
        )
        user_id = Heroku.account().id
        headers = {
            "User-Agent": useragent,
            "Authorization": f"Bearer {HEROKU_API_KEY}",
            "Accept": "application/vnd.heroku+json; version=3.account-quotas",
        }
        path = "/accounts/" + user_id + "/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        if r.status_code != 200:
            return await die.edit_text("`Error: something bad happened`\n\n" f">.`{r.reason}`\n")
        result = r.json()
        quota = result["account_quota"]
        quota_used = result["quota_used"]

        """ - Used - """
        remaining_quota = quota - quota_used
        percentage = math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)
        day = math.floor(hours / 24)

        """ - Current - """
        App = result["apps"]
        try:
            App[0]["quota_used"]
        except IndexError:
            AppQuotaUsed = 0
            AppPercentage = 0
        else:
            AppQuotaUsed = App[0]["quota_used"] / 60
            AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)
        await asyncio.sleep(1.5)

        return await die.edit_text(
            "❂ **Dyno Usage **:\n\n"
            f" » Dyno usage for **{HEROKU_APP_NAME}**:\n"
            f"      •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
            f"**|**  [`{AppPercentage}`**%**]"
            "\n\n"
            "  » Dyno hours quota remaining this month:\n"
            f"      •  `{hours}`**h**  `{minutes}`**m**  "
            f"**|**  [`{percentage}`**%**]"
            f"\n\n  » Dynos heroku {day} days left"
        )
    
    else:
        await message.reply_text("This is SUDO restricted command.")

@Client.on_message(command("logs"))
async def logs(_, message: Message):
    if message.from_user.id in SUDO_USERS:
        chat = message.chat
        user = message.from_user
        with open("ShikimoriMusic_logs.txt", "rb") as f:
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
        user = await pbot.get_users(user_id)
        user = (
            user.first_name if not user.mention else user.mention
        )
        reply += f"• {user}\n"
    await m.delete()
    await message.reply_animation(img, caption=reply, parse_mode="html")
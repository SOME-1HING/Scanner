from functools import wraps
import html
import time
from datetime import datetime
from io import BytesIO

from telegram import ChatMemberAdministrator, Update, Chat, ChatMember
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden, TelegramError
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import mention_html

from ShikimoriMusic import pbot
from ShikimoriMusic.plugins.extraction import extract_user_and_text, extract_user
from ShikimoriMusic.vars import OWNER_ID, SUPPORT_CHAT, SUDO_USERS
from ShikimoriMusic.setup.filters import command
from ShikimoriMusic.mongo import global_bans_db as db

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
async def gban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id, reason = await extract_user_and_text(message, context, args)

    if not user_id:
        await message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect..",
        )
        return

    if int(user_id) in SUDO_USERS:
        await message.reply_text(
            "That user is part of the Association\nI can't act against our own.",
        )
        return

    if int(user_id) in SUDO_USERS:
        await message.reply_text(
            "I spy, with my little eye... a disaster! Why are you guys turning on each other?",
        )
        return

    if user_id == bot.id:
        await message.reply_text("You uhh...want me to punch myself?")
        return

    if user_id in [777000, 1087968824]:
        await message.reply_text("Fool! You can't attack Telegram's native tech!")
        return

    try:
        user_chat = await bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            await message.reply_text("I can't seem to find this user.")
            return ""
        return

    if user_chat.type != "private":
        await message.reply_text("That's not a user!")
        return

    if db.is_user_gbanned(user_id):

        if not reason:
            await message.reply_text(
                "This user is already gbanned; I'd change the reason, but you haven't given me one...",
            )
            return

        old_reason = db.update_gban_reason(
            user_id,
            user_chat.username or user_chat.first_name,
            reason,
        )
        if old_reason:
            await message.reply_text(
                "This user is already gbanned, for the following reason:\n"
                "<code>{}</code>\n"
                "I've gone and updated it with your new reason!".format(
                    html.escape(old_reason),
                ),
                parse_mode=ParseMode.HTML,
            )

        else:
            await message.reply_text(
                "This user is already gbanned, but had no reason set; I've gone and updated it!",
            )

        return

    await message.reply_text("On it!")

    start_time = time.time()
    datetime_fmt = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    if chat.type != "private":
        chat_origin = "<b>{} ({})</b>\n".format(html.escape(chat.title), chat.id)
    else:
        chat_origin = "<b>{}</b>\n".format(chat.id)

    log_message = (
        f"#GBANNED\n"
        f"<b>Originated from:</b> <code>{chat_origin}</code>\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>Banned User:</b> {mention_html(user_chat.id, user_chat.first_name)}\n"
        f"<b>Banned User ID:</b> <code>{user_chat.id}</code>\n"
        f"<b>Event Stamp:</b> <code>{current_time}</code>"
    )

    if reason:
        if chat.type == chat.SUPERGROUP and chat.username:
            log_message += f'\n<b>Reason:</b> <a href="https://telegram.me/{chat.username}/{message.message_id}">{reason}</a>'
        else:
            log_message += f"\n<b>Reason:</b> <code>{reason}</code>"

    db.gban_user(user_id, user_chat.username or user_chat.first_name, reason)

    end_time = time.time()
    gban_time = round((end_time - start_time), 2)

    if gban_time > 60:
        gban_time = round((gban_time / 60), 2)
        await message.reply_text("Done! Gbanned.", parse_mode=ParseMode.HTML)
    else:
        await message.reply_text("Done! Gbanned.", parse_mode=ParseMode.HTML)

    try:
        await bot.send_message(
            user_id,
            "#EVENT"
            "You have been marked as Malicious and as such have been banned from any future groups we manage."
            f"\n<b>Reason:</b> <code>{html.escape(user.reason)}</code>"
            f"</b>Appeal Chat:</b> @{SUPPORT_CHAT}",
            parse_mode=ParseMode.HTML,
        )
    except:
        pass  # bot probably blocked by user


@sudo_plus
async def ungban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id = await extract_user(message, context, args)

    if not user_id:
        await message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect..",
        )
        return

    user_chat = await bot.get_chat(user_id)
    if user_chat.type != "private":
        await message.reply_text("That's not a user!")
        return

    if not db.is_user_gbanned(user_id):
        await message.reply_text("This user is not gbanned!")
        return

    await message.reply_text(
        f"I'll give {user_chat.first_name} a second chance, globally."
    )

    start_time = time.time()
    datetime_fmt = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    if chat.type != "private":
        chat_origin = f"<b>{html.escape(chat.title)} ({chat.id})</b>\n"
    else:
        chat_origin = f"<b>{chat.id}</b>\n"

    log_message = (
        f"#UNGBANNED\n"
        f"<b>Originated from:</b> <code>{chat_origin}</code>\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>Unbanned User:</b> {mention_html(user_chat.id, user_chat.first_name)}\n"
        f"<b>Unbanned User ID:</b> <code>{user_chat.id}</code>\n"
        f"<b>Event Stamp:</b> <code>{current_time}</code>"
    )

    db.ungban_user(user_id)

    end_time = time.time()
    ungban_time = round((end_time - start_time), 2)

    if ungban_time > 60:
        ungban_time = round((ungban_time / 60), 2)
        await message.reply_text(f"Person has been un-gbanned. Took {ungban_time} min")
    else:
        await message.reply_text(f"Person has been un-gbanned. Took {ungban_time} sec")


@sudo_plus
async def gbanlist(update: Update, context: CallbackContext):
    banned_users = db.get_gban_list()

    if not banned_users:
        await update.effective_message.reply_text(
            "There aren't any gbanned users! You're kinder than I expected...",
        )
        return

    banfile = "Screw these guys.\n"
    for user in banned_users:
        banfile += f"[x] {user['name']} - {user['user_id']}\n"
        if user["reason"]:
            banfile += f"Reason: {user['reason']}\n"

    with BytesIO(str.encode(banfile)) as output:
        output.name = "gbanlist.txt"
        await update.effective_message.reply_document(
            document=output,
            filename="gbanlist.txt",
            caption="Here is the list of currently gbanned users.",
        )
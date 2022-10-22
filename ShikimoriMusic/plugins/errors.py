from functools import wraps
import html
import io
import random
import sys
import time
import traceback

import pretty_errors
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Chat, ChatMember
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, ContextTypes

from ShikimoriMusic import application
from ShikimoriMusic.vars import SUDO_USERS
from ShikimoriMusic.plugins.carbon_helper import paste

pretty_errors.mono()

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

class ErrorsDict(dict):
    "A Magical Element To Store Errors"

    def __init__(self, *args, **kwargs):
        self.raw = []
        super().__init__(*args, **kwargs)

    def __contains__(self, error):
        self.raw.append(error)
        error.identifier = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))
        for e in self:
            if type(e) is type(error) and e.args == error.args:
                self[e] += 1
                return True
        self[error] = 0
        return False

    def __len__(self):
        return len(self.raw)


errors = ErrorsDict()


async def error_callback(update: Update, context: CallbackContext):
    if not update:
        return
    if context.error not in errors:
        try:
            stringio = io.StringIO()
            pretty_errors.output_stderr = stringio
            output = pretty_errors.excepthook(
                type(context.error),
                context.error,
                context.error.__traceback__,
            )
            pretty_errors.output_stderr = sys.stderr
            pretty_error = stringio.getvalue()
            stringio.close()
        except:
            pretty_error = "Failed to create pretty error."
        tb_list = traceback.format_exception(
            None,
            context.error,
            context.error.__traceback__,
        )
        tb = "".join(tb_list)
        pretty_message = (
            "{}\n"
            "-------------------------------------------------------------------------------\n"
            "An exception was raised while handling an update\n"
            "User: {}\n"
            "Chat: {} {}\n"
            "Callback data: {}\n"
            "Message: {}\n\n"
            "Full Traceback: {}"
        ).format(
            pretty_error,
            update.effective_user.id,
            update.effective_chat.title if update.effective_chat else "",
            update.effective_chat.id if update.effective_chat else "",
            update.callback_query.data if update.callback_query else "None",
            update.effective_message.text if update.effective_message else "No message",
            tb,
        )
        e = html.escape(f"{context.error}")
        link = await paste(pretty_message)
        await context.bot.send_message(
            -1001717154437,
            text=f"#{context.error.identifier}\n<b>An Error has occurred:"
            f"</b>\n<code>{e}</code>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("See Errors", url=link)]],
            ),
            parse_mode=ParseMode.HTML,
        )


async def list_errors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in SUDO_USERS:
        return
    e = {
        k: v for k, v in sorted(errors.items(), key=lambda item: item[1], reverse=True)
    }
    msg = "<b>Errors List:</b>\n"
    for x in e:
        msg += f"• <code>{x}:</code> <b>{e[x]}</b> #{x.identifier}\n"
    msg += f"{len(errors)} have occurred since startup."
    if len(msg) > 4096:
        with open("errors_msg.txt", "w+") as f:
            f.write(msg)
        await context.bot.send_document(
            update.effective_chat.id,
            open("errors_msg.txt", "rb"),
            caption=f"Too many errors have occured..",
            parse_mode="html",
        )
        return
    await update.effective_message.reply_text(msg, parse_mode="html")


@sudo_plus
async def logs(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    with open("Emily_logs.txt", "rb") as f:
        await context.bot.send_document(document=f, filename=f.name, chat_id=user.id)
    if chat.type != chat.PRIVATE:
        msg = update.effective_message
        hmm = await msg.reply_text(
            "`Logs sent. Check your pm.`", parse_mode=ParseMode.MARKDOWN
        )
        time.sleep(10)
        try:
            msg.delete()
            hmm.delete()
        except BadRequest:
            pass


application.add_error_handler(error_callback)
application.add_handler(CommandHandler("errors", list_errors))
application.add_handler(CommandHandler(("logs", "log"), logs, block=False))

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ShikimoriMusic.vars import SUPPORT_CHAT
from ShikimoriMusic import BOT_USERNAME


@Client.on_callback_query(filters.regex("home"))
async def home(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""ᴡᴇʟᴄᴏᴍᴇ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})

ɪ ᴀᴍ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ᴀɴᴅ ᴜsᴇғᴜʟ ғᴇᴀᴛᴜʀᴇs.

ᴜsᴇ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ !!""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🗂 ᴄᴏᴍᴍᴀɴᴅs", callback_data="cmds"),
                    InlineKeyboardButton(
                        "🆘 ʜᴇʟᴘ", url=f"https://t.me/{SUPPORT_CHAT}")
                ],
                [
                    InlineKeyboardButton(
                        "✚ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
           ]
        ),
    )
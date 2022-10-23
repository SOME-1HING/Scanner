from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.types import Message

from Scanner import pbot
from Scanner.vars import SUDO_USERS

async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await pbot.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


async def authorised(message):
    chatID = message.chat.id
    return 0

async def unauthorised(message: Message):
    chatID = message.chat.id
    checking = message.from_user.mention
    text = (
        f"**ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs !!**"
        + f"\n❌ Delete Message Chats"
    )
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await pbot.leave_chat(chatID)
    return 1

async def adminsOnly(permission, message):
    chatID = message.chat.id
    if not message.from_user:
        if message.sender_chat:
            return await authorised(message)
        return await unauthorised(message)
    userID = message.from_user.id
    permissions = await member_permissions(chatID, userID)
    if userID not in SUDO_USERS and permission not in permissions:
        return await unauthorised(message)
    return await authorised(message)

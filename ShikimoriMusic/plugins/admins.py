from asyncio import QueueEmpty

from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

from pyrogram import filters
from pyrogram.types import Message

from ShikimoriMusic import pbot
from ShikimoriMusic.mongo.queue import (
    is_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from ShikimoriMusic.calls import calls
from ShikimoriMusic.setup.filters import command, other_filters
from ShikimoriMusic.calls.queues import clear, get, is_empty, task_done


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


from ShikimoriMusic.setup.administrator import adminsOnly


@pbot.on_message(command(["pause"]) & other_filters)
async def pause(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not is_active_chat(chat_id):
        return await message.reply_text(
            "• ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ❌"
        )
    elif not is_music_playing(message.chat.id):
        return await message.reply_text(
            "• ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ❌"
        )
    music_off(chat_id)
    await calls.pytgcalls.pause_stream(chat_id)
    await message.reply_text(
        f"• ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ▶️ ᴘᴀᴜsᴇᴅ\n• ᴀᴅᴍɪɴ : {checking}"
    )


@pbot.on_message(command(["resume"]) & other_filters)
async def resume(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not is_active_chat(chat_id):
        return await message.reply_text(
            "❌ __**I dont think if something's paused on voice chat**__"
        )
    elif is_music_playing(chat_id):
        return await message.reply_text(
            "❌ __**I dont think if something's paused on voice chat**__"
        )
    else:
        music_on(chat_id)
        await calls.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            f"• ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ⏸ ʀᴇsᴜᴍᴇᴅ\n• ᴀᴅᴍɪɴ : {checking}"
        )


@pbot.on_message(command(["end"]) & other_filters)
async def stop(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        remove_active_chat(chat_id)
        await calls.pytgcalls.leave_group_call(chat_id)
        await message.reply_text(
            f"• ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ❌ sᴛᴏᴘᴘᴇᴅ\n• ᴀᴅᴍɪɴ : {checking}"
        )
    else:
        return await message.reply_text(
            "❌ __**I dont think if something's playing on voice chat**__"
        )


@pbot.on_message(command(["skip"]) & other_filters)
async def skip(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not is_active_chat(chat_id):
        await message.reply_text("❌ __**Nothing's playing on voice chat**__")
    else:
        task_done(chat_id)
        if is_empty(chat_id):
            remove_active_chat(chat_id)
            await message.reply_text(
                "❌ __**No more music in Queue**__\n\n**»** `Leaving Voice Chat...`"
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await calls.pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        get(chat_id)["file"],
                    ),
                ),
            )
            await message.reply_text(
                f"• ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ⏯ sᴋɪᴘᴘᴇᴅ\n• ᴀᴅᴍɪɴ : {checking}"
            )


@pbot.on_message(filters.command(["cleandb"]))
async def stop_cmd(_, message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chat_id = message.chat.id
    checking = message.from_user.mention
    try:
        clear(chat_id)
    except QueueEmpty:
        pass
    remove_active_chat(chat_id)
    try:
        await calls.pytgcalls.leave_group_call(chat_id)
    except:
        pass
    await message.reply_text(
        f"✅ __Erased queues in **{message.chat.title}**__\n│\n╰ Database cleaned by {checking}"
    )

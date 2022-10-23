import datetime
import platform
import time
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from Scanner.mongo.global_bans_db import num_gbanned_users
from Scanner.setup.filters import command
from pyrogram import __version__ as pyrover
from pyrogram.types import Message
    
from Scanner import starttime, pbot
from  Scanner.vars import SUDO_USERS, SUPPORT_CHAT

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

@pbot.on_message(command("stats"))
async def stats(_, message: Message):
    if message.from_user.id in SUDO_USERS:
        uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        botuptime = get_readable_time((time.time() - starttime))
        status = "**「❍」Sʏsᴛᴇᴍ Sᴛᴀᴛɪsᴛɪᴄs「❍」**\n\n✦"
        status += f"**┈➤ Sʏsᴛᴇᴍ Sᴛᴀʀᴛ Tɪᴍᴇ: ** `{str(uptime)}`\n✦"
        uname = platform.uname()
        status += f"**┈➤ Sʏsᴛᴇᴍ:** `{str(uname.system)}`\n✦"
        status += f"**┈➤ Nᴏᴅᴇ Nᴀᴍᴇ:** `{(str(uname.node))}`\n✦"
        status += f"**┈➤ Rᴇʟᴇᴀsᴇ:** `{(str(uname.release))}`\n✦"
        status += f"**┈➤ Mᴀᴄʜɪɴᴇ:** `{(str(uname.machine))}`\n✦"
        mem = virtual_memory()
        cpu = cpu_percent()
        disk = disk_usage("/")
        status += f"**┈➤ Cᴘᴜ:** `{str(cpu)} %`\n✦"
        status += f"**┈➤ Rᴀᴍ:** `{str(mem[2])} %`\n✦"
        status += f"**┈➤ Sᴛᴏʀᴀɢᴇ:** `{str(disk[3])} %`\n\n✦"
        status += f"**┈➤ Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ:** `{python_version()}`\n✦"
        status += f"**┈➤ Pʏʀᴏɢʀᴀᴍ Vᴇʀsɪᴏɴ:** `{str(pyrover)}`\n✦"
        status += f"**┈➤ Uᴘᴛɪᴍᴇ:** `{str(botuptime)}`\n"

        img = "https://telegra.ph/file/a0f299ae4eba53370ce8b.mp4"
        await message.reply_animation(
            img,
            caption = status
            + "\n\n**「✪」Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs「✪」**:\n\n✦"
            + f"**┈➤ Scanned Users:** `{num_gbanned_users()}`\n✦" 

            + f"\n\n    [✦ ꜱᴜᴘᴘᴏʀᴛ ✦](https://t.me/{SUPPORT_CHAT})\n"
            + " ┗━━✦❘༻           ༺❘✦━━┛",
            parse_mode="markdown",
        )
    else:
        await message.reply_text("This is SUDO restricted command.")
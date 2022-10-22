from re import A
import aiofiles
from ShikimoriMusic.mongo.chats import add_served_chat, is_served_chat
import ffmpeg
import asyncio
import os
import requests
import yt_dlp
import aiohttp

from PIL import Image, ImageFont, ImageDraw, ImageFilter

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant

from ShikimoriMusic.calls import calls, queues
from ShikimoriMusic.calls.youtube import download
from ShikimoriMusic.calls import convert as cconvert
from ShikimoriMusic.mongo.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
)
from ShikimoriMusic import pbot, ubot
from ShikimoriMusic.vars import (
    DURATION_LIMIT,
    LOG_CHANNEL,
    que,
    SUPPORT_CHAT,
    UPDATE,
)
from ShikimoriMusic import ASS_USERNAME, BOT_ID, ASS_NAME, ASS_ID, BOT_NAME, BOT_USERNAME
from ShikimoriMusic.setup.filters import command
from ShikimoriMusic.setup.errors import DurationLimitError
from ShikimoriMusic.setup.gets import get_url, get_file_name

# plus
chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
flex = {}

error_img = "https://telegra.ph/file/71f03e109851d4ced2e38.mp4"
loading_img = "https://telegra.ph/file/18e11c12e62c846ef0572.mp4"
down_img = "https://telegra.ph/file/1fa311f95574d532395a2.mp4"

def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 27:        
            text1 += " " + i
        elif len(text2) + len(i) < 25:        
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1,text2]

# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def mask_circle_solid(pil_img, background_color, blur_radius, offset=0):
    background = Image.new(pil_img.mode, pil_img.size, background_color)

    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    return Image.composite(pil_img, background, mask)

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image = Image.open("etc/img.jpg")
    thumb = Image.open(f"./background.png")
    image1 = changeImageSize(1280, 720, image)
    image11 = changeImageSize(1280, 720, thumb)
        
    image3 = image11.resize((350,350))

    im_thumb = mask_circle_solid(image3, (0, 0, 0), 4)
    im_thumb1 = mask_circle_solid(image11, (0, 0, 0), 4)
        
    image1.paste(im_thumb, (805,180))
    image11.paste(im_thumb1, (805,180))

    # fonts
    font3 = ImageFont.truetype(r'etc/robot.otf', 40)
    font4 = ImageFont.truetype(r'etc/Mukta-ExtraBold.ttf', 35)

    image4 = ImageDraw.Draw(image1)

    # title
    title1 = truncate(title)
    image4.text((150, 225), text=title1[0], fill="white", font = font3, align ="left") 
    image4.text((150, 280), text=title1[1], fill="white", font = font3, align ="left") 

    # description
    views = f"Views : {views}"
    duration = f"Duration : {duration} minutes"
    channel = f"Request : {BOT_NAME} Bot"

    image4.text((175, 410), text=views, fill="white", font = font4, align ="left") 
    image4.text((175, 460), text=duration, fill="white", font = font4, align ="left") 
    image4.text((175, 510), text=channel, fill="white", font = font4, align ="left")

    image1.save(f"final.png")
    os.remove(f"background.png")
    final = f"temp.png"
    return final
     



# play
@Client.on_message(
    command(["play", f"play@{BOT_USERNAME}"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    user_id = message.from_user.id
    chid = message.chat.id 

    if not is_served_chat(chid):
        try:
            add_served_chat(chid)
            pass
        except:
            pass

    if message.sender_chat:
        return await message.reply_text(
            " __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )

    if message.chat.id in DISABLED_GROUPS:
        await message.reply(
            " __**Music player is turned off, ask the admin to turn on it on!**__"
        )
      

        return
    lel = await pbot.send_animation(chid, loading_img,caption="**ᴘʀᴏᴄᴇssɪɴɢ.....**")


    c = await pbot.get_chat_member(message.chat.id, BOT_ID)
    if c.status != "administrator":
        lel.delete()
        lel = await pbot.send_animation(chid,error_img, caption = f"**ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀ ᴀᴅᴍɪɴ !!**"
        )
        return
    if not c.can_manage_voice_chats:
        lel.delete()
        lel = await pbot.send_animation(chid,
            error_img, caption="**ᴍᴀɴᴀɢᴇ-ᴠᴏɪᴄᴇ-ᴄʜᴀᴛ : ᴘᴏᴡᴇʀ ❌**"
        )
        return
    if not c.can_delete_messages:
        lel.delete()
        lel = await pbot.send_animation(chid,
            error_img, caption="**ᴅᴇʟᴇᴛᴇ-ᴍᴇssᴀɢᴇ : ᴘᴏᴡᴇʀ ❌**"
        )
        return
    if not c.can_invite_users:
        lel.delete()
        lel = await pbot.send_animation(chid,
            error_img, caption="**ɪɴᴠɪᴛᴇ-ᴜsᴇʀs : ᴘᴏᴡᴇʀ ❌**"
        )
        return

    try:
        b = await pbot.get_chat_member(message.chat.id, ASS_ID)
        if b.status == "kicked":
            await message.reply_animation(
                error_img, caption=f"🔴 {ASS_NAME} (@{ASS_USERNAME}) is banned in your chat **{message.chat.title}**\n\nUnban it first to use music"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ubot.join_chat(f"{message.chat.username}")
                await message.reply(
                    f"**@{ASS_USERNAME} joined !**",
                )
                remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_animation(
                    error_img, caption=f"**@{ASS_USERNAME} failed to join** Add @{ASS_USERNAME} manually in your group.\n\n**Reason**:{e}"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    kontol = (invite_link.replace("+", "")).split("t.me/")[1]
                    link_bokep = f"https://t.me/joinchat/{kontol}"
                await ubot.join_chat(link_bokep)
                await message.reply(
                    f"**@{ASS_USERNAME} joined successfully**",
                )
                remove_active_chat(message.chat.id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_animation(
                    error_img, caption=f"**@{ASS_USERNAME} failed to join** Add @{ASS_USERNAME} manually in your group.\n\n**Reason**:{e}"
                )

    await message.delete()
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"💡 Audio longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        url = f"https://t.me/{UPDATE}"
        title = audio.title
        thumb_name = "https://i.imgur.com/W6AuXQ9.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("🎥 ᴡᴀᴛᴄʜ", url="https://youtube.com"),
            InlineKeyboardButton("📨 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        ],[
            InlineKeyboardButton("🚫 ᴄʟᴏsᴇ", callback_data="cls"),
        ],
        
    ]
)

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await cconvert(
            (await message.reply_to_message.download(file_name))
            if not os.path.isfile(os.path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("🎥 ᴡᴀᴛᴄʜ", url="https://youtube.com"),
            InlineKeyboardButton("📨 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        ],[
            InlineKeyboardButton("🚫 ᴄʟᴏsᴇ", callback_data="cls"),
        ],
        
    ]
)

        except Exception as e:
            title = "NaN"
            thumb_name = "https://i.imgur.com/W6AuXQ9.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="YouTube 🎬", url="https://youtube.com")]]
            )

        if (dur / 60) > DURATION_LIMIT:
            lel.delete()
            lel = await pbot.send_animation(chid,
                error_img,caption =f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.delete()
                            lel = pbot.send_animation(chid,
                                loading_img, caption= f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ {title[:50]}\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.delete()
                            lel = pbot.send_animation(chid,loading_img, caption= f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ :** {title[:50]}..\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.delete()
                            lel = pbot.send_animation(chid,loading_img, caption= f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ** {title[:50]}...\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.delete()
                            lel = pbot.send_animation(chid,loading_img, caption=  f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ :** {title[:50]}....\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.delete()
                lel = pbot.send_animation(chid,loading_img, caption=  f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ :** {title[:50]}.....\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴛɪᴍᴇ :** {taken} sec\n\n**ᴄᴏɴᴠᴇʀᴛɪɴɢ ғɪʟᴇ : **[__FFmpeg processing__]"
                )
                print(f"[{url_suffix}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, url, my_hook)
        file_path = await cconvert(x)
    else:
        if len(message.command) < 2:
            await lel.delete()
            return await pbot.send_animation(chid,
                error_img, caption= "❌ ᴀʟsᴏ ɢɪᴠᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ ᴡɪᴛʜ ᴜsɪɴɢ ᴘʟᴀʏ ᴄᴏᴍᴍᴀɴᴅ !!\n\nғᴏʀ ᴇxᴀᴍᴘʟᴇ :\n/play 295"
            )
        await asyncio.sleep(2)
        await lel.delete()
        lel = await pbot.send_animation(chid, loading_img, caption = "**ғɪɴᴅɪɴɢ 🔎 sᴇʀᴠᴇʀ !!**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await asyncio.sleep(2)
        await lel.delete()
        lel = await pbot.send_animation(chid,loading_img, caption= "**ɢᴇᴛᴛɪɴɢ..... ʀᴇsᴘᴏɴsᴇ.....**")


        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            ydl_opts = {"format": "bestaudio[ext=m4a]"}

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await asyncio.sleep(2)
            await lel.delete()
            lel = await pbot.send_animation(chid,
                error_img, caption= "• **Song not found**\n\nwrite name correctly."
            )
            print(str(e))
            return

        if (dur / 60) > DURATION_LIMIT:
            await asyncio.sleep(2)
            await lel.delete()
            lel = await pbot.send_animation(chid,
                error_img, caption= f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        await lel.delete()

        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)

            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            return
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎙 **sᴏɴɢ**: [{title[:35]}]({link})\n🎬 **sᴏᴜʀᴄᴇ**: YouTube\n⏱️ **ᴅᴜʀᴀᴛɪᴏɴ**: `{duration}`\n👁‍🗨 **ᴠɪᴇᴡs**: `{views}`\n📤 **ᴜᴘʟᴏᴀᴅᴇʀ**: @{BOT_USERNAME}"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        hm = await pbot.send_audio(
            LOG_CHANNEL,
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )

        lel = await message.reply_text("Here You Goo.....")

        audio = (
            (hm.audio or hm.voice)
            if hm
            else None
        )

        file_name = get_file_name(audio)
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await cconvert(
            (await hm.download(file_name))
            if not os.path.isfile(os.path.join("downloads", file_name))
            else file_name
        )
        keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("🎥 ᴡᴀᴛᴄʜ", url=f"{url}"),
            InlineKeyboardButton("📨 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        ],[
            InlineKeyboardButton("🚫 ᴄʟᴏsᴇ", callback_data="cls"),
        ],
        
    ]
)
    if is_active_chat(message.chat.id):
        position = await queues.put(message.chat.id, file=file_path)
        await asyncio.sleep(2)
        await pbot.send_photo(
            chid,
            photo="final.png",
            reply_markup=keyboard,
            caption="**[ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴠɪᴀ ʏᴏᴜᴛᴜʙᴇ 📡]({})**\n\n• ᴜsᴇʀ : {}\n• ɢʀᴏᴜᴘ : [{}](https://t.me/{})".format(
                url, message.from_user.mention(), message.chat.title, message.chat.username
            ),
        )
    else:
        try:
            await calls.pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception:
            await lel.delete()
            lel = await pbot.send_animation(chid,loading_img, caption= "Error Joining Voice Chat. Make sure Voice Chat is Enabled.\n\n If YES, then make sure Music Bots Assistant is not banned in your group or available in your group!"
            )
            return lel
    

        music_on(message.chat.id)
        add_active_chat(message.chat.id)
        await asyncio.sleep(2)
        await pbot.send_photo(
            chid,
            photo="final.png",
            reply_markup=keyboard,
            caption="**[ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴠɪᴀ ʏᴏᴜᴛᴜʙᴇ 📡]({})**\n\n• ᴜsᴇʀ : {}\n• ɢʀᴏᴜᴘ : [{}](https://t.me/{})".format(
                url, message.from_user.mention(), message.chat.title, message.chat.username
            ),
        )

    os.remove("final.png")
    await hm.delete()
    return await lel.delete()

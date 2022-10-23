import aiohttp
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import aiofiles
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant
from pyrogram import Client
from telethon import events
from telethon import *
from telethon.tl.functions.account import *
from telethon.tl.functions.channels import *
from telethon.tl.functions.photos import *
from telethon.tl.types import *
from html import *

from telegraph import Telegraph, exceptions, upload_file

from ShikimoriMusic import ASS_USERNAME, BOT_ID, ASS_NAME, ASS_ID, BOT_NAME, BOT_USERNAME, LOGGER, pbot, tbot
from ShikimoriMusic.setup.filters import command

Hero = "Scanner"
telegraph = Telegraph()
r = telegraph.create_account(short_name=Hero)
auth_url = r["auth_url"]

# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(user, user_dp):
    async with aiohttp.ClientSession() as session:
        async with session.get(user_dp) as resp:
            if resp.status == 200:
                f = await aiofiles.open("user_dp.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    LOGGER.info("e1")
    image = Image.open("etc/info_img.jpg")
    dp = Image.open(f"./user_dp.png")
    image1 = changeImageSize(300, 424, image)
    image11 = changeImageSize(247, 180, dp)
        
        
    image1.paste(image11, (26,90))

    # fonts
    font3 = ImageFont.truetype(r'etc/robot.otf', 40)

    image4 = ImageDraw.Draw(image1)

    LOGGER.info("e2")
    # title
    image4.text((60, 320), text=user.first_name, fill="white", font = font3, align ="left") 
    image4.text((60, 360), text=user.id, fill="white", font = font3, align ="left") 

    image1.save(f"{user.id}.png")
    LOGGER.info("e3")
    return
    
def tgm_uploder(file):
    Error = None
    Link = None
    try:
        media_urls = upload_file(file)
    except exceptions.TelegraphException as exc:
        Error = "ERROR: " + str(exc)
    else:
        Link = f"https://telegra.ph{media_urls[0]}"

    return Link, Error

@tbot.on(events.NewMessage(pattern="^[!/]info$"))
async def PPScmd(event):
#        """Gets the profile photos of replied users, channels or chats"""
    try:
        user = await event.get_reply_message()
        if user:
            photos = await event.client.get_profile_photos(user.sender)
            
            photo = await event.client.download_media(photos[0], "./")
            await tbot.send_file(event.chat.id, photo)
            link, error = tgm_uploder(photo)
            await tbot.send_message(f"{link} + {error}")
            await generate_cover(user.sender, link)
            await tbot.send_file(event.chat.id, f"{user.sender.id}.png")
            LOGGER.info(f"{user.sender.id}.png")
        else:
            await tbot.send_message(event.chat.id, "Reply to user mate")
            
    except:
        await tbot.send_message(event.chat.id, "Error")

        


@tbot.on(events.NewMessage(pattern="^[!/]pfp$"))
async def PPScmd(event):
#        """Gets the profile photos of replied users, channels or chats"""
    try:
        id = "".join(event.raw_text.split(maxsplit=2)[1:]) 
        user = await event.get_reply_message()
        if user:
            photos = await event.client.get_profile_photos(user.sender)
        else:
            photos = await event.client.get_profile_photos(event.chat_id)
        if id.strip() == "":
            try:
                await event.client.send_file(event.chat.id, photos)
            except:
                photo = await event.client.download_profile_photo(event.chat_id)
                await tbot.send_file(event.chat.id, photo)
        else:
            try:
                id = int(id)
                if id <= 0:
                    await event.edit("<code>ID number you entered is invalid</code>")
                    return
            except:
                await event.edit("<code>ID number you entered is invalid</code>")
                return
            if int(id) <= (len(photos)):
                send_photos = await event.client.download_media(photos[id - 1])
                await tbot.send_file(event.chat.id, send_photos)
            else:
                await event.edit("<code>No photo found with that id</code>")
                return
    except:
        await tbot.send_message("Reply to user mate")

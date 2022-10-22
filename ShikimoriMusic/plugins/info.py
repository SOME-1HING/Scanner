import aiohttp
from PIL import Image, ImageFont, ImageDraw, ImageFilter

from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant
from pyrogram import Client

from ShikimoriMusic import ASS_USERNAME, BOT_ID, ASS_NAME, ASS_ID, BOT_NAME, BOT_USERNAME, pbot, tbot
from ShikimoriMusic.setup.filters import command

# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(first_name, user_id):
    user_pic = []
    async for photo in tbot.get_profile_photos(user_id):
       user_pic.append(photo)
    user_dp = user_pic[0] 
    image = Image.open("etc/info_img.jpg")
    image1 = changeImageSize(300, 424, image)
    image11 = changeImageSize(247, 180, user_dp)
        
        
    image1.paste(image11, (26,90))

    # fonts
    font3 = ImageFont.truetype(r'etc/robot.otf', 40)

    image4 = ImageDraw.Draw(image1)

    # title
    image4.text((60, 320), text=first_name, fill="white", font = font3, align ="left") 
    image4.text((60, 360), text=user_id, fill="white", font = font3, align ="left") 

    image1.save(f"final.png")
    final = f"temp.png"
    return final

@Client.on_message(command("info"))
async def info(client: Client, message: Message):
    user = message.from_user
    profile = await generate_cover(user.first_name, user.id)
    message.reply_photo(profile, caption="hmm")
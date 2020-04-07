from os.path import sep
import io

import discord
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps


def to_discord_file(image, name="image"):
    # return byte array to send
    byte_arr = io.BytesIO()
    image.save(byte_arr, format="webp")
    fp = io.BytesIO(byte_arr.getvalue())
    return discord.File(fp=fp, filename=f"{name}.webp")


def get_user_img(user, size=256, mask=None):
    """Takes a discord user and returns a PIL image of their pfp.
    Size must be a power of 2 between 16 and 1024.
    """
    url = user.avatar_url_as(static_format="webp", size=size)
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))

    # Draw Circular Mask
    if mask == "circle":
        masksize = (size, size)
        mask = Image.new('L', masksize, 0)  # Black/White
        maskdraw = ImageDraw.Draw(mask)
        maskdraw.ellipse((0, 0) + masksize, fill=255)

        image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        image.putalpha(mask)

    return image


def draw_versus(p1, p2):
    """Draws a versus image to start the match"""
    canvas_width = 537
    canvas_height = 300

    # Create new canvas
    background = Image.new(
        mode="RGBA",
        size=(canvas_width, canvas_height),
        color=(0, 0, 0, 0)
    )

    d = ImageDraw.Draw(background)  # set image for drawing
    fnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 30)

    # load versus
    versus = Image.open(f"assets{sep}RedVersus.png")
    versus.thumbnail((192, 192), Image.ANTIALIAS)

    # get discord pfps
    avatar1 = get_user_img(p1, mask="circle")
    avatar2 = get_user_img(p2, mask="circle")

    # # Draw Circular Mask
    # masksize = (256, 256)
    # mask = Image.new('L', masksize, 0)  # Black/White
    # maskdraw = ImageDraw.Draw(mask)
    # maskdraw.ellipse((0, 0) + masksize, fill=255)

    # # cut circles out of pfps
    # avatar1 = ImageOps.fit(avatar1, mask.size, centering=(0.5, 0.5))
    # avatar1.putalpha(mask)
    # avatar2 = ImageOps.fit(avatar2, mask.size, centering=(0.5, 0.5))
    # avatar2.putalpha(mask)

    # Calculate offsets
    versus_offset = (canvas_width//2 - versus.size[0]//2,
                     128-versus.size[1]//2)
    avatar2_offset = (canvas_width - avatar2.size[0] + 0, 0)

    # paste images on background
    background.paste(avatar1, (0, 0), avatar1)
    background.paste(avatar2, avatar2_offset, avatar2)
    background.paste(versus, versus_offset, versus)

    # Draw names
    name1width, _ = d.textsize(p1.name, fnt)
    name2width, _ = d.textsize(p2.name, fnt)
    name1pos = (128 - name1width/2, 266)
    name2pos = ((canvas_width-128) - name2width/2, 266)
    d.text(name1pos, p1.name, font=fnt, fill=(255, 255, 255, 255))
    d.text(name2pos, p2.name, font=fnt, fill=(255, 255, 255, 255))

    return background


def draw_winner(winner, **kwargs):
    c_width = 900
    c_height = 410

    # assets
    avatar = get_user_img(winner, mask="circle")
    crown = Image.open(f"assets{sep}crown.png")
    crown.thumbnail((256, 256), Image.ANTIALIAS)

    # Create new canvas
    background = Image.new(
        mode="RGBA",
        size=(c_width, c_height),
        color=(0, 0, 0, 0)
    )
    d = ImageDraw.Draw(background)  # set image for drawing
    titlefnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 50)
    textfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 40)

    background.paste(avatar, (120, 150), avatar)
    background.paste(crown, (0, 0), crown)

    d.text((450, 100), f"{winner.name} Wins!",
           font=titlefnt, fill=(255, 255, 255, 255))

    for i, item in enumerate(kwargs.items(), 1):
        stat_height = 110 + (i * 50)  # 100, 150, 200 -->
        stat = f"{item[0]}: {item[1]}"
        d.text((450, stat_height), stat,
               font=textfnt, fill=(255, 255, 255, 255))

    return background

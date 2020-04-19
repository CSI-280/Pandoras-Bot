"""Commands related to the user profile such a customization."""
import math
import os
from os.path import sep

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

from classes import Player
from vars import bot
from drawing import to_discord_file


class ShopCommands(commands.Cog):
    """Store related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shop", aliases=["store"])
    async def shop_navigation(self, ctx, *, destination=""):
        """Navigation command for the shop."""

        if destination.strip().lower() == "banners":
            command = bot.get_command("shopbanners")
            return await ctx.invoke(command)
        elif destination.strip().lower() == "titles":
            command = bot.get_command("shoptitles")
            return await ctx.invoke(command)
        elif destination.strip().lower() == "cards":
            command = bot.get_command("shopcards")
            return await ctx.invoke(command)
        else:
            command = bot.get_command("shophome")
            return await ctx.invoke(command)

    @commands.command(name="shophome", hidden=True)
    async def shop_home(self, ctx):
        """Displays the home page of the shop"""
        p = ctx.prefix
        player = Player.get(ctx.author.id)

        home_embed = discord.Embed(
            title="Pandora's Shop", description=f"Balance: {player.pbucks}")
        home_embed.add_field(
            name="Banners", value=f"`{p}shop banners`", inline=False)
        home_embed.add_field(
            name="Titles", value=f"`{p}shop titles`", inline=False)
        home_embed.add_field(
            name="Cards", value=f"`{p}shop cards`", inline=False)
        await ctx.send(embed=home_embed)

    @commands.command(name="shopbanners", hidden=True)
    async def shop_banners(self, ctx):
        """Displays the banner shop"""
        file = to_discord_file(draw_shop_header(12345, "Banners"))
        await ctx.send(file=file)

    @commands.command(name="shoptitles", hidden=True)
    async def shop_titles(self, ctx):
        """Displays the title shop"""
        await ctx.send("Coming Soon")

    @commands.command(name="shopcards", hidden=True)
    async def shop_cards(self, ctx):
        """Displays the card shop"""
        await ctx.send("Coming Soon")


def setup(bot):
    bot.add_cog(ShopCommands(bot))


def draw_shop_header(balance, description):
    """Draws the image pasted to the top of each shop page."""
    IMGW, IMGH = 900, 150
    PADDING_TOP = 10
    # Create new canvas
    header = Image.new(
        mode="RGBA",
        size=(IMGW, IMGH),
        color=(0, 0, 0, 128)
    )
    titlefont = ImageFont.truetype(f"assets{sep}Roboto.ttf", 60)
    descfont = ImageFont.truetype(f"assets{sep}Roboto.ttf", 40)
    d = ImageDraw.Draw(header)

    # Draw title
    title = "Pandora's Shop"
    titlex, titley = titlefont.getsize(title)
    title_offset = (IMGW//2 - titlex//2, PADDING_TOP)
    d.text(title_offset, title, font=titlefont)

    # Draw description
    descx, _ = descfont.getsize(description)
    desc_offset = (IMGW//2 - descx//2, PADDING_TOP*2 + titley)
    d.text(desc_offset, description, font=descfont)

    # Draw balance
    balance = "{:,}".format(balance)
    bal_offset = (5, 5)
    d.text(bal_offset, balance, font=descfont)

    return header


# def draw_banner_shop(player):
#     # Banner dims
#     BWIDTH, BHEIGHT = 400, 100
#     BMIDDLE = BHEIGHT//2
#     MID_PADDING = 10
#     ROWS = math.ceil(len(self.banners)/2)
#     IMGW = BWIDTH*2+MID_PADDING
#     IMGH = ROWS * (BHEIGHT + MID_PADDING) - MID_PADDING

#     # Create new canvas
#     background = Image.new(
#         mode="RGBA",
#         size=(IMGW, IMGH),
#         color=self.card_background
#     )
#     font = ImageFont.truetype(f"assets{sep}Roboto.ttf", 30)

#     for i, name in enumerate(self.banners):
#         row = i // 2 * BHEIGHT + MID_PADDING * (i//2)  # 00112233
#         col = i % 2 * BWIDTH  # 01010101

#         if i % 2 == 1:
#             col += MID_PADDING

#         if i // 2 != 0:
#             row + MID_PADDING

#         banner = Image.open(f"assets{sep}banners{sep}{name}.png")
#         banner = banner.resize((BWIDTH, BHEIGHT))
#         d = ImageDraw.Draw(banner)

#         _, texty = font.getsize(name)
#         text_offset = (BWIDTH//10, BMIDDLE - texty//2)
#         d.text(text_offset, name, font=font)

#         background.paste(banner, (col, row))
#     return background

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
        await ctx.send("Coming Soon")

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

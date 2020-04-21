"""Commands related to the user profile such a customization."""

import discord
import os
from os.path import sep
from discord.ext import commands
from rapidfuzz import process

import database as db
from auth import authorize
from classes import Player
from vars import bot
from drawing import to_discord_file


class ProfileCommands(commands.Cog):
    """Profile stuff."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="register")
    async def register_player(self, ctx):
        """Registers a player"""
        try:
            Player.get(ctx.author.id)
        except:
            new_player = Player(ctx.author.id)
            await ctx.send("You in")
            return db.update(new_player)

        raise commands.UserInputError("Already registered")

    ############### SHOW PLAYER INFO ###############

    @commands.command(name="card")
    async def show_player_card(self, ctx, *, pid=None):
        """Shows a player's game card"""

        # Check message mentions
        if ctx.message.mentions:
            pid = ctx.message.mentions[0].id
        # Check user input
        elif pid and pid.isdigit():
            pid = int(pid)
        else:
            pid = ctx.author.id

        # Get player and draw card of desired id
        card = Player.get(pid).draw_card()
        await ctx.send(file=to_discord_file(card))

    @commands.command(name="banners")
    async def show_player_banners(self, ctx):
        """Show a player's collected banners."""
        player = Player.get(ctx.author.id)
        file = to_discord_file(player.draw_banners())
        await ctx.send(content=f"{player.name}'s Banners", file=file)

    @commands.command(name="titles")
    async def show_player_titles(self, ctx):
        """Show a player's collected titles."""
        player = Player.get(ctx.author.id)
        title_embed = discord.Embed(
            title=f"{player.name}'s Titles",
            description='\n'.join(player.titles))

        await ctx.send(embed=title_embed)

    ############### SET PLAYER INFO ###############

    @commands.command(name="setbanner", aliases=["sb"])
    async def set_player_banner(self, ctx, *, banner):
        """Set a players active banner."""
        player = Player.get(ctx.author.id)

        all_banners = (f[0:-4] for f in os.listdir(f"assets{sep}banners"))
        banner = process.extractOne(banner, all_banners, score_cutoff=80)

        if not banner:
            raise commands.UserInputError(
                f"That banner doesn't exist. Check for banners with the `{ctx.prefix}shop banners` command.")
        elif banner[0] not in player.banners:
            raise commands.UserInputError("You don't own that banner.")
        else:
            player.banner = banner[0]
            await ctx.send(content=f"Success:", file=to_discord_file(player.draw_banner()))
            db.update(player)

    @commands.command(name="settitle", aliases=["st"])
    async def set_player_title(self, ctx, *, title):
        """Set a players active title"""
        player = Player.get(ctx.author.id)

        # Match an available title
        all_titles = Player.EXTRA_TITLES + Player.TITLES
        title = process.extractOne(title, all_titles, score_cutoff=80)

        if not title:
            raise commands.UserInputError(
                f"That title doesn't exist. You can set this as a custom title with X command")
        elif title[0] not in player.titles:
            raise commands.UserInputError("You don't own that title")
        else:
            player.title = title[0]
            await ctx.send(content=f"Success:", file=to_discord_file(player.draw_banner()))
            return db.update(player)


def setup(bot):
    bot.add_cog(ProfileCommands(bot))

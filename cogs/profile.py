import discord
from discord.ext import commands

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
        authorize(ctx, "registered")

        new_player = Player(ctx.author.id)
        await ctx.send("Registration SUCCessful! UwU")
        db.update(new_player)

    @commands.command(name="registerbot")
    async def registerbot(self, ctx):
        if ctx.author.id != 128595549975871488:
            return
        new_player = Player(bot.user.id)
        await ctx.send("Registration SUCCessful! UwU")
        db.update(new_player)

    @commands.command(name="card")
    async def show_player_card(self, ctx):
        """Shows a player's game card"""
        player = Player.get(ctx.author.id)
        card = player.draw_card()
        await ctx.send(file=to_discord_file(card))


def setup(bot):
    bot.add_cog(ProfileCommands(bot))

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

    @commands.command(name="card")
    async def show_player_card(self, ctx, *, pid=None):
        """Shows a player's game card"""

        # Get the right id
        if ctx.message.mentions:
            print("mentioned")
            pid = ctx.message.mentions[0].id
        elif pid and pid.isdigit():
            pid = int(pid)
        else:
            pid = ctx.author.id

        # Get player and draw card of desired id
        authorize(ctx, player=pid)
        player = Player.get(pid)
        card = player.draw_card()
        await ctx.send(file=to_discord_file(card))


def setup(bot):
    bot.add_cog(ProfileCommands(bot))

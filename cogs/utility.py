"""Commands that are not for the user.
The are strictly for use of the devs and testing
"""

import discord
from discord.ext import commands

import classes
import database as db
from drawing import to_discord_file
from vars import bot


class UtilityCommands(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="write", aliases=["w"])
    async def repeat_message(self, ctx, *, msg=""):
        """repeats whatever message is sent"""
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(name="sb")
    async def scoreboardasdlkjfa(self, ctx, *, gains=40):
        """repeats whatever message is sent"""
        game = classes.Game.get(ctx.channel.id)
        img = game.draw_scoreboard()

        await ctx.send(file=to_discord_file(img))

    @commands.command(name="registerbot", aliases=["botregister"])
    async def registerbot(self, ctx):
        if ctx.author.id != 128595549975871488:
            return
        new_player = classes.Player(bot.user.id)
        await ctx.send("Registration SUCCessful! UwU")
        db.update(new_player)


def setup(bot):
    bot.add_cog(UtilityCommands(bot))

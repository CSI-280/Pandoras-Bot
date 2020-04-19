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

    @commands.command(name="updateall")
    async def update_all(self, ctx):
        """Update all entries in the data base"""
        players = list(classes.Player._players.values())
        guilds = list(classes.Guild._guilds.values())
        db.update(*players)
        db.update(*guilds)
        await ctx.send("DONE")

    @commands.command(name="write", aliases=["w"])
    async def repeat_message(self, ctx, *, msg=""):
        """repeats whatever message is sent"""
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(name="registerbot", aliases=["botregister"])
    async def registerbot(self, ctx):
        if ctx.author.id != 128595549975871488:
            return
        new_player = classes.Player(bot.user.id)
        await ctx.send("Registration SUCCessful! UwU")
        db.update(new_player)

    @commands.command(name="deletelocal")
    async def delete_local_instance(self, ctx, *, id):
        if ctx.author.id != 128595549975871488:
            return
        try:
            del classes.Player._players[int(id)]
        except KeyError:
            pass
        await ctx.send("Player deleted")


def setup(bot):
    bot.add_cog(UtilityCommands(bot))

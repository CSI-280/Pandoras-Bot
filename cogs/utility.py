"""Commands that are not for the user.
The are strictly for use of the devs and testing
"""

import discord
from discord.ext import commands

from vars import bot


class UtilityCommands(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="print", aliases=["write", "repeat", "p"])
    async def repeat_message(self, ctx, *, msg=""):
        """repeats whatever message is sent"""
        await ctx.message.delete()
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(UtilityCommands(bot))

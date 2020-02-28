import discord
from discord.ext import commands

from vars import bot


class BaseCommands(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        """The standard help command."""
        await ctx.send("Doesn't exist yet")

    @commands.command(name='howdy')
    async def howdy(self, ctx):
        """Says howdy!"""
        await ctx.send(f"Howdy, {ctx.message.author.mention}!")


def setup(bot):
    bot.add_cog(BaseCommands(bot))

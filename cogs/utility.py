"""Commands that are not for the user.
The are strictly for use of the devs and testing
"""

import discord
from discord.ext import commands

from vars import bot

import classes
from drawing import to_discord_file


class UtilityCommands(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="print", aliases=["write", "repeat", "p", "w"])
    async def repeat_message(self, ctx, *, msg=""):
        """repeats whatever message is sent"""
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(name="sb")
    async def scoreboardasdlkjfa(self, ctx, *, gains=40):
        """repeats whatever message is sent"""
        player = classes.Player.get(ctx.author.id)
        # banner = player.draw_banner()
        # xpbar = player.draw_xp(gains=int(gains))
        # card = player.draw_card(gains=int(gains))
        game = classes.Game.get(ctx.channel.id)
        img = game.draw_scoreboard()

        await ctx.send(file=to_discord_file(img))


def setup(bot):
    bot.add_cog(UtilityCommands(bot))

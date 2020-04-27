import random

import discord
from discord.ext import commands
from discord.ext.commands import UserInputError

from vars import bot, get_help
from sender import PaginatedEmbed

import drawing


class BaseCommands(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, *, page="0"):
        """The standard help command."""

        # get prefix and generate help dictionary
        help_dict = get_help(ctx.prefix)

        if not page.isdigit() or not -1 < int(page) < len(help_dict):
            raise commands.UserInputError(
                f"Invalid page number. Number must be between 0-{len(help_dict)-1}")

        pages = PaginatedEmbed(content=help_dict, pointer=int(page))
        await pages.send(ctx.channel)

    @commands.command(name='howdy')
    async def howdy(self, ctx):
        """Say howdy!"""
        await ctx.send(f"Howdy, {ctx.author.mention}!")

    @commands.command(name="game_list")
    async def game_list(self, ctx):

        # Prints out the list of games
        await ctx.send("""\
            !======== [List of Games] ========!

            Game #1
            TicTacToe   : !tictactoe OR !t OR !ttt

            Game #2
            Hangman     :  !h

            Game #3
            Battleship  :  !bs
            """)

    @commands.command(name="coinflip", aliases=["flipcoin", "cf"])
    async def flip_coin(self, ctx):
        """Returns a random choice between head or tails."""
        await ctx.send(f"**{random.choice(('Heads', 'Tails'))}**")

    @commands.command(name="rolldie", aliases=["dieroll", "rd"])
    async def roll_dice(self, ctx):
        """Returns a random side of a die"""
        values = list(range(1, 7))
        await ctx.send(f"**{random.choice(values)}**")


def setup(bot):
    bot.add_cog(BaseCommands(bot))

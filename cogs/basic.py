import discord
from discord.ext import commands
from discord.ext.commands import UserInputError

from vars import bot, get_prefix, get_help


class BaseCommands(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, *, page="help"):
        """The standard help command."""
        # get prefix and generate help dictionary
        help_dict = get_help(ctx.prefix)

        if page == "1":
            page = "commands"

        help_info = help_dict.get(page)

        # Raise is argument isn't found
        if not help_info:
            raise UserInputError(f"**{page}** is an invalid argument")

        # Generate embed
        help_embed = discord.Embed(title=help_info["title"],
                                   description=help_info["description"],
                                   color=discord.Colour.blue())

        # Add fields to embed
        for k, v in help_info["fields"].items():
            help_embed.add_field(name=k, value=v, inline=False)

        # send embed to channel
        await ctx.send(embed=help_embed)

    @commands.command(name='howdy')
    async def howdy(self, ctx):
        """Says howdy!"""
        await ctx.send(f"Howdy, {ctx.author.mention}!")


    @commands.command(name = "game_list")
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


def setup(bot):
    bot.add_cog(BaseCommands(bot))

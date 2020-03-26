"""Module for handling errors caught by discord.ext.commands.CommandError."""

import sys
import traceback

import discord
from discord.ext import commands

from vars import bot, get_prefix


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command."""
        error = getattr(error, 'original', error)

        # skip if command is invalid
        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(ctx.channel, discord.channel.DMChannel):
            return await ctx.send(f"**{ctx.command}** must be used in a server channel")

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"Your command is missing a required argument")

        elif isinstance(error, commands.UserInputError):
            return await ctx.send(error)

        # If error is not caught then show the ugly error code
        error_embed = discord.Embed(title=f'Your command: {ctx.message.content}',
                                    description=str(error),
                                    color=discord.Colour.red())

        await ctx.send(embed=error_embed)

        # send to devs too
        error_channel = bot.get_channel(692427334803914813)
        await error_channel.send(embed=error_embed)

        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))

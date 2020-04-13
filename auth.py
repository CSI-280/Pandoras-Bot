"""Module for holding custom errors and also checks
for the bot to run before functions.
"""

from discord.ext.commands import CommandError, UserInputError

import classes  # dodging circular imports


class MissingGuild(CommandError):
    """Error for not finding a guild"""
    pass


def authorize(ctx, *checks, **input_checks):
    """Check certain perms and assure passing."""
    guild = classes.Guild.get(ctx.guild.id)

    # Check if a user was mentioned
    if "mentions" in checks and not ctx.message.mentions:
        raise UserInputError(
            "You need to mention a user for that command to work")

    return True

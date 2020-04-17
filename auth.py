"""Module for holding custom errors and also checks
for the bot to run before functions.
"""

from discord.ext.commands import CommandError, UserInputError

import classes  # dodging circular imports


class MissingGuild(CommandError):
    """Error for not finding a guild"""
    pass


class RegistrationError(CommandError):
    pass


def authorize(ctx, *checks, **input_checks):
    """Check certain perms and assure passing."""

    # Check if a user was mentioned
    if "mentions" in checks and not ctx.message.mentions:
        raise UserInputError(
            "You need to mention a user for that command to work")

    if "registered" in checks and ctx.author.id in classes.Player._players:
        raise RegistrationError("Already Registered")

    return True

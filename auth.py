"""Module for holding custom errors and also checks
for the bot to run before functions.
"""

from discord.ext.commands import CommandError, UserInputError

import classes  # dodging circular imports


class MissingGuild(CommandError):
    """Error for not finding a guild"""
    pass


class NotFoundError(UserInputError):
    """Raised when player/guild is not found. Strict"""
    pass


class PlayerLookupError(UserInputError):
    """Raised when player lookup is not successful"""
    pass


class RegistrationError(CommandError):
    """Raised when player is already registered or not registered"""
    pass


def authorize(ctx, *args, **kwargs):
    """Check certain perms and assure passing."""

    # Check if a user was mentioned
    if "mentions" in args and not ctx.message.mentions:
        raise UserInputError(
            "You need to mention a user for that command to work")

    if "registered" in args and ctx.author.id in classes.Player._players:
        raise RegistrationError("Already Registered")

    if "player" in kwargs and kwargs["player"] not in classes.Player._players:
        raise PlayerLookupError("Couldn't find that player")

    return True

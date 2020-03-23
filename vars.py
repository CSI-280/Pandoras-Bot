import discord
from discord.ext import commands

extensions = [
    "cogs.basic",
]


def get_prefix(bot, message):
    """Gets the server prefix."""
    return "!"


bot = commands.Bot(command_prefix=get_prefix,
                   help_command=None)  # creates bot object


def get_help(p):
    """Places prefixes into a help dictionary."""
    return {
        "help": {
            "title": "Pandora's Bot Help",
            "description": (f"Table of Contents\n"
                            f"To go to another page please use `{p}help <page>`\n"
                            f"Example `{p}help 1`, `{p}help setup`"),
            "fields": {"1. Commands": "General, Non-game related commands",
                       "-----------------------------": "[Github](https://github.com/CSI-280/Pandoras-Bot)"}

        },
        "commands": {
            "title": "Pandora's Bot General Commands",
            "description": f"on a specific command you can use `{p}help <command>`",
            "fields": {
                "General Commands":
                    (f"`{p}howdy`: You've got a friend in me\n"
                     f"`{p}prefix`: Not yet implemented"),
            }

        }
    }

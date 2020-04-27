import discord
from discord.ext import commands

###################### BOT RELATED STUFF ######################

extensions = [
    "cogs.basic",
    "cogs.errors",
    "cogs.utility",

    # Cosmetic stuff
    "cogs.profile",
    "cogs.shop",

    # Games
    "cogs.games.tictactoe",
    "cogs.games.rps"
]

emoji_dict = {"checkmark": "✅",
              "crossmark": "❌",
              "left_arrow": "⬅️",
              "right_arrow": "➡️",
              "home_arrow": "↩️",
              "up_arrow": "🔼",
              "down_arrow": "🔽",
              "double_down": "⏬",
              "refresh": "🔄",
              "updown": "↕️"}


def get_prefix(bot, message):
    """Gets the server prefix."""
    return "!"


bot = commands.Bot(command_prefix=get_prefix,
                   help_command=None)  # creates bot object

###################### HELP RELATED STUFF ######################


def get_help(p):
    """Places prefixes into a help dictionary."""
    return {
        "home": {
            "title": "Pandora's Bot Help",
            "description": f"Navigate between pages with the reaction buttons or use `{p}help <page>`",
            "1. Commands": "General, Non-game related commands",
            "2. Games": "A list of games you can play",
            "-----------------------------": "[Github](https://github.com/CSI-280/Pandoras-Bot)"
        },
        "commands": {
            "title": "Pandora's Commands",
            "description": " ",
            "Commands": "list of commands go here",
        },
        "gamelist": {
            "title": "Pandora's Games",
            "description": " ",
            "TicTacToe": "play with `!t`, `!ttt`",
            "Hangman": "play with `!h`, `!hm`",
            "Battleship": "play with `!bs`"
        }
    }

import discord
from discord.ext import commands

extensions = [
    "cogs.basic",
    ]

bot = commands.Bot(command_prefix="!", help_command=None) # creates bot object
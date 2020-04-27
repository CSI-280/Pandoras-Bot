import discord
from discord.ext import commands
import json
import os

from classes import Guild
import database as db
from env import TOKEN
from vars import bot, extensions, get_prefix


@bot.event
async def on_ready():
    """Initial function to run when the bot is ready to function"""
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing,
                                  name="@Pandora's Bot for help"))

    print("Generating Objects...")

    # collect new guild ids and create objects for them
    new_ids = {guild.id for guild in bot.guilds} - set(Guild._guilds.keys())

    # Create new Guild objects
    new_guilds = [Guild(id) for id in new_ids]

    print("Updating database...")
    db.update(*new_guilds)

    print("Ready Player One.")


@bot.event
async def on_message(message):
    """Message listener."""
    # make sure it doesnt run when bot writes message
    if message.author == bot.user:
        return

    await bot.process_commands(message)  # checks if message is command


@bot.event
async def on_guild_join(guild):
    """Bot joined a new server"""
    guild = Guild(guild.id)
    db.update(guild)


@bot.event
async def on_guild_remove(guild):
    """Bot was removed from a server"""
    Guild.pop(guild.id, None)

    # remove from DB
    db.delete_guild(guild.id)

# loads extensions(cogs) listed in vars.py
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Couldn't load {extension}")
            print(e)

bot.run(TOKEN)  # runs the bot

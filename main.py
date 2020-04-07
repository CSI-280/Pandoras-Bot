import discord
from discord.ext import commands
import json
import os

from classes import Guild, Gamer
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
    for id in new_ids:
        new_gamers = [Gamer(id=member.id, guild_id=id)
                      for member in bot.get_guild(id).members]
        Guild(id=id, prefix='!', gamers=new_gamers)

    print("Ready Player One.")


@bot.event
async def on_message(message):
    """Message listener."""
    # make sure it doesnt run when bot writes message
    if message.author == bot.user:
        return

    # Get and send prefix
    # if message.mentions and message.mentions[0].id == bot.user.id:
    #     await message.channel.send(f"{get_prefix(bot, message)}help")

    await bot.process_commands(message)  # checks if message is command


@bot.event
async def on_guild_join(guild):
    """Bot joined a new server"""
    pass


@bot.event
async def on_guild_remove(guild):
    """Bot was removed from a server"""
    pass


@bot.event
async def on_member_join(member):
    """Someone joined a server"""


@bot.event
async def on_member_remove(member):
    """Someone left a server"""
    pass


# loads extensions(cogs) listed in vars.py
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"Couldn't load {extension}")

bot.run(os.environ["TOKEN"])  # runs the bot

import discord
from discord.ext import commands
import json
import os

from classes import Guild, Member
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
    db.getall()  # get and build returning guilds

    # collect new guild ids and create objects for them
    new_ids = {guild.id for guild in bot.guilds} - set(Guild._guilds.keys())

    # Create new Guild objects
    new_guilds = []
    for id in new_ids:
        new_members = {member.id: Member(member.id, id)
                       for member in bot.get_guild(id).members}
        new_guilds.append(Guild(id=id, members=new_members))

    print("Updating database...")
    db.update(*new_guilds)

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
    new_members = {member.id: Member(member.id, guild.id)
                   for member in guild.members}
    guild = Guild(id=id, members=new_members)
    db.update(guild)


@bot.event
async def on_guild_remove(guild):
    """Bot was removed from a server"""
    Guild.pop(guild.id, None)
    db.delete_one(guild.id)


@bot.event
async def on_member_join(member):
    """Someone joined a server"""
    guild = Guild.get(member.guild.id)
    guild.members[member.id] = Member(member.id, guild.id)
    db.update(guild)


@bot.event
async def on_member_remove(member):
    """Someone left a server"""
    guild = Guild.get(member.guild.id)
    guild.members.pop(member.id, None)
    db.update(guild)


# loads extensions(cogs) listed in vars.py
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Couldn't load {extension}")
            print(e)

bot.run(TOKEN)  # runs the bot

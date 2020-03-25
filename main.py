import discord
from discord.ext import commands
import json
import os

from vars import bot, extensions, get_prefix

client = commands.Bot(command_prefix = '!')


@bot.event
async def on_ready():
    """Initial function to run when the bot is ready to function"""
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing,
                                  name="@Pandora's Bot for help"))
    print("Ready Player One.")


@bot.event
async def on_message(message):
    """Message listener."""
    # make sure it doesnt run when bot writes message
    if message.author == bot.user:
        return

    # Get and send prefix
    if message.mentions and message.mentions[0].id == bot.user.id:
        await message.channel.send(f"{get_prefix(bot, message)}help")

    await bot.process_commands(message)  # checks if message is command


@client.event
async def user_join(member):
    """Open player data and write new data for level system."""
    with open('users.json', 'r') as f:
        users = json.load(f)

    # Make an await command for updating the data.

    # Write the new data.
    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_win(player):
    """Add experience to the winner of a game"""
    with open('users.json', 'r') as f:
        users = json.load(f)

    # Make an await command for updating the data, adding experience, and leveling up.
    # Specify the amount of xp to give the user.

    # Write the new data.
    with open('users.json', 'w') as f:
        json.dump(users, f)


async def update_data(users, user):
    """Add new users if they don't already exist and set default xp and level along with their name."""


async def add_experience(users, user, xp):
    """Add the specified amount of xp."""


async def level_up(users, user, channel):
    """Check to see if a user leveled up and update if true"""

# loads extensions(cogs) listed in vars.py
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"Couldn't load {extension}")

bot.run(os.environ["TOKEN"])  # runs the bot

import discord
from discord.ext import commands
import os

from vars import bot, extensions, get_prefix


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


# loads extensions(cogs) listed in vars.py
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"Couldnt load {extension}")

bot.run(os.environ["TOKEN"])  # runs the bot

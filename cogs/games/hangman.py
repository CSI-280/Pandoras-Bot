import discord
from discord.ext import commands
from discord.ext.commands import UserInputError

from vars import bot, get_prefix, get_help
from auth import authorize

import random
import json

# A small list to use for guessing.
word_list = ("cat", "dog", "telephone", "apple", "television")

# Basic name to get the game working. Will need to change to get a user.
name = "calvin"

print("User " + name + " has started a game of hangman.")


class Game:
    """Class for playing the game"""
    # Max amount of times someone can guess incorrectly
    turns = 10
    guesses = ''
    word = random.choice(word_list)

    while turns > 0:
        print("Guesses left: " + str(turns))
        failed = 0
        for char in word:
            if char in guesses:
                print(char)
            else:
                print("_")
                failed += 1
        if failed == 0:
            print("User " + name + " has won hangman.")
            break
        guess = input("Guess a character: ")
        guesses += guess
        if guess not in word:
            turns -= 1
            print("That character is not in the word")
        if turns == 0:
            print("User " + name + " has lost a game of hangman.")


class Hangman(commands.Cog):
    """Handles the commands associated with the game"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hangman", aliases=["h", "hm"])
    async def hangman(self, ctx):

        """Starts up a game of hangman"""
        authorize(ctx, "mentions")  # check for a mentioned user

        p1 = ctx.author
        p2 = ctx.message.mentions[0]  # first mentioned user

        if p1 == p2:
            raise UserInputError("Can't play against yourself")

def setup(bot):
    bot.add_cog(Hangman(bot))
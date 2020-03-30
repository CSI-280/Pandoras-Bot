import discord
from discord.ext import commands
import random
import json

# A small list to use for guessing.
word_list = ("cat", "dog", "telephone", "apple", "television")

# Basic name to get the game working. Will need to change to get a user.
name = "calvin"

print("User " + name + " has started a game of hangman.")

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

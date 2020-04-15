import os
import sys
from pymongo import MongoClient
import classes
from vars import bot
from env import MONGO_PASS, BOT_VERSION

# database setup
client = MongoClient(
    f"mongodb+srv://pandorasbot:{MONGO_PASS}@cluster0-wglq9.mongodb.net/test?retryWrites=true&w=majority")
db = client.PandorasBotDB

if BOT_VERSION == "real":
    print("Using REAL")
    guild_coll = db.PandorasBotGuilds
    player_coll = db.PandorasBotPlayers
else:
    print("Using TEST")
    guild_coll = db.PandorasBotGuildsTest
    player_coll = db.PandorasBotPlayersTest


def update(*objects):
    """
    Update the linked mongoDB database. Updates all if arg is left blank.

    Args:
        guilds (list of Guild): list of guild to update
    """

    for obj in objects:
        if isinstance(obj, classes.Guild):
            coll = guild_coll
        else:
            coll = player_coll

        data = obj.to_json()  # serialize objects

        # find a document based on ID and update update
        if coll.find_one({"id": obj.id}):
            if not coll.find_one(data):
                coll.find_one_and_update({"id": obj.id}, {"$set": data})
        else:
            # add new document if guild is not found
            coll.insert_one(data)


def getall():
    """Generates objects from json format to python objects from mongoDB

    Only runs on start of program
    """
    classes.Guild._guilds.clear()  # remove all guilds to be remade
    data = list(guild_coll.find())  # get mongo data

    for guild_dict in data:
        classes.Guild.from_json(guild_dict)  # build guild

    classes.Player._players.clear()
    data = list(player_coll.find())

    for player_dict in data:
        classes.Player.from_json(player_dict)

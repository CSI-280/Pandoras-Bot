import os
import sys
from pymongo import MongoClient
from classes import Guild
from vars import bot
from env import MONGO_PASS

# database setup
client = MongoClient(
    f"mongodb+srv://pandorasbot:{MONGO_PASS}@cluster0-wglq9.mongodb.net/test?retryWrites=true&w=majority")
db = client.PandorasBotDB
coll = db.PandorasBotData


def update(*guilds):
    """
    Update the linked mongoDB database. Updates all if arg is left blank.

    Args:
        guilds (list of Guild): list of guild to update
    """
    for guild in guilds:
        json_data = guild.to_json()  # serialize objects

        # find a document based on ID and update update
        if coll.find_one({"id": guild.id}):
            if not coll.find_one(json_data):
                coll.find_one_and_update({"id": guild.id}, {"$set": json_data})
        else:
            # add new document if guild is not found
            coll.insert_one(json_data)


def getall():
    """Generates objects from json format to python objects from mongoDB

    Only runs on start of program
    """
    Guild._guilds.clear()  # remove all guilds to be remade
    data = list(coll.find())  # get mongo data

    for guild_dict in data:
        Guild.from_json(guild_dict)  # build guild


def delete_one(id):
    """Deletes a document from the database"""
    coll.delete_one({"id": id})

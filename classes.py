"""Module for holding class structure for the bot to use."""

import discord

import auth
from vars import bot


class Guild:
    """Guild object that stores preferences for a guild the bot is in

    Args:
        name (str): The name of the guild
        id (int): The id of the guild from discord
        prefix (str): The custom guild command prefix

    Attributes:
        _guilds (dict, int:Guild): Stores all of the created guilds
        name (str): The name of the guild
        id (int): The id of the guild from discord
        prefix (str): The custom guild command prefix
    """
    _guilds = {}  # dict of guilds that have been created

    def __init__(self, id, prefix, gamers):
        self.name = str(bot.get_guild(id))
        self.id = id
        self.prefix = prefix
        self.gamers = gamers
        Guild._guilds[id] = self  # add guild to the dict

    @property
    def dguild(self):
        """Returns the discord.py version of the guild"""
        return bot.get_guild(self.id)

    @classmethod
    def get(cls, id):
        """Find guild in the dictionary."""
        guild = cls._guilds.get(id)
        if not guild:
            raise auth.MissingGuild()
        return guild

    def to_json(self):
        """Convert a guild to valid JSON format"""
        return {
            "name": self.name,
            "id": self.id,
            "prefix": self.prefix,
            "gamers": [gamer.to_json() for gamer in self.gamers]
        }

    @staticmethod
    def from_json(data):
        """Convert valid JSON to guild object."""
        return Guild(
            id=data["id"],
            prefix=data["prefix"],
            gamers=data["gamers"]
        )


class Gamer:
    """Has information on each member of a server

    Args:
        id (int): the members discord id
        guild_id (int): The id of the guild the member belongs to

    Attributes:
        id (int): the members discord id
        guild_id (int): The id of the guild the member belongs to
    """

    def __init__(self, id, guild_id):
        self.name = str(bot.get_user(id))
        self.id = id
        self.guild_id = guild_id

    @property
    def guild(self):
        return Guild.get(self.guild_id)

    def to_json(self):
        """Convert Color object to valid JSON."""
        return {
            "id": self.id,
            "guild_id": self.guild_id
        }

    @staticmethod
    def from_json(member):
        """Create Theme object from valid JSON"""
        return Gamer(
            id=member["id"],
            guild_id=member["guild_id"]
        )

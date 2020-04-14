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

    def __init__(self, id, **kwargs):
        self.name = str(bot.get_guild(id))
        self.id = id
        self.prefix = kwargs.get("prefix", "!")
        Guild._guilds[id] = self  # add guild to the dict

    @property
    def dguild(self):
        """Returns the discord.py version of the guild"""
        return bot.get_guild(self.id)

    ################## CLASS METHODS ##################

    @classmethod
    def get(cls, id):
        """Find guild in the dictionary."""
        guild = cls._guilds.get(id)
        if not guild:
            raise auth.MissingGuild()
        return guild

    @classmethod
    def pop(cls, id, alt=None):
        """Pop a value off the dict list"""
        return cls._guilds.pop(id, alt)

    ################## JSON CONVERSION ##################

    def to_json(self):
        """Convert a guild to valid JSON format"""
        return {
            "id": self.id,
            "prefix": self.prefix
        }

    @staticmethod
    def from_json(data):
        """Convert valid JSON to guild object."""
        return Guild(
            id=data["id"],
            prefix=data["prefix"],
        )


class Player:
    """Global stats

    Args:
        id (int): the members discord id
        guild_id (int): The id of the guild the member belongs to

    Attributes:
        id (int): the members discord id
        guild_id (int): The id of the guild the member belongs to
    """
    _players = {}

    DEFAULT_STATS = {
        "tictactoe": 0,
        "hangman": 0,
        "battleship": 0,
        "rps": 0  # Rock Paper Scissors
    }

    XP_MULTIPLIERS = {
        "tictactoe": .1,
        "hangman": .2,
        "battleship": 1,
        "rps": .05  # Rock Paper Scissors
    }

    XP_VALUES = {
        True: 100,
        False: 20
    }

    RANK_THRESHOLD = 20

    TITLES = ("Benda", "Noob", "Amateur", "Experienced",
              "Skilled", "Expert", "Semi-Pro", "Pro")
    EXTRA_TITLES = ("He Who Hands Claps", "Sherpa",
                    "I'm a 1700", "I Don't Lose", "GC", "The Placer", "Edumacated", "The Prodigy",
                    "Born Champion", "Godly", "Unbelievably Talented", "Nut", "Swanson")

    def __init__(self, id, **kwargs):
        self.name = str(bot.get_user(id))
        self.id = id
        self.xp = kwargs.get("xp", 0)
        self.title = kwargs.get("title", "Benda")
        self.titles = kwargs.get("titles", ["Benda"])

        # stats
        self.games_played = kwargs.get("games_played", Player.DEFAULT_STATS)
        self.wins = kwargs.get("wins", Player.DEFAULT_STATS)  # fat W's
        self.draws = kwargs.get("draws", Player.DEFAULT_STATS)
        Player._players[id] = self

    @property
    def losses(self):
        """The losses the player has."""
        return {k: self.games_played[k] - self.wins[k] - self.draws[k] for k in self.wins.keys()}

    @property
    def ratio(self):
        """The Win-Loss ratio for the player."""
        return {k: self.wins[k] / self.losses[k] for k in self.wins.keys()}

    @property
    def most_played(self):
        """Returns the most played game."""
        return max(self.games_played, key=self.games_played.get)

    @classmethod
    def get(cls, id):
        player = cls._players.get(id)
        if not player:
            raise auth.RegistrationError("Not Registered")
        return player

    ################## STAT MANAGEMENT ##################

    def update(self, game, won=False, draw=False):
        """Update a player."""
        print(f"updating {self.name}")
        old_xp = self.xp
        self.xp += Player.XP_MULTIPLIERS[game] * Player.XP_VALUES[won]

        # Acquire new title if needed
        if int(old_xp) // Player.RANK_THRESHOLD != int(self.xp) // Player.RANK_THRESHOLD:
            print("TITLE SWITCH")
            self.title = Player.TITLES[int(self.xp // Player.RANK_THRESHOLD)]
            self.titles.append(self.title)

        # update games played
        self.games_played[game] += 1
        if won:
            self.wins[game] += 1
        elif draw:
            self.draws[game] += 1

    ################## JSON CONVERSION ##################

    def to_json(self):
        """Convert Color object to valid JSON."""
        return {
            "id": self.id,
            "xp": self.xp,
            "title": self.title,
            "titles": self.titles,
            "games_played": self.games_played,
            "wins": self.wins,
            "draws": self.draws
        }

    @staticmethod
    def from_json(player):
        """Create Theme object from valid JSON"""
        return Player(
            id=player["id"],
            xp=player.get("xp", 0),
            title=player.get("title", "Benda"),
            titles=player.get("titles", ["Benda"]),
            games_played=player.get("games_played", Player.DEFAULT_STATS),
            wins=player.get("wins", Player.DEFAULT_STATS),
            draws=player.get("draws", Player.DEFAULT_STATS)
        )

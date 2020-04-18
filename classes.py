"""Module for holding class structure for the bot to use."""
import math
from itertools import cycle, islice
from os.path import sep
from random import randint

import discord
from PIL import Image, ImageDraw, ImageFont

import auth
import database as db
import drawing
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

    RANK_THRESHOLD = 1000

    TITLES = ("Benda", "Noob", "Amateur", "Experienced",
              "Skilled", "Expert", "Semi-Pro", "Pro")
    EXTRA_TITLES = ("He Who Hands Claps", "Sherpa",
                    "I'm a 1700", "I Don't Lose", "GC", "The Placer", "Edumacated", "The Prodigy",
                    "Born Champion", "Godly", "Unbelievably Talented", "Nut", "Swanson")

    def __init__(self, id, **kwargs):
        self.name = str(bot.get_user(id).name)
        self.id = id
        self.xp = kwargs.get("xp", 0)
        self.banner = kwargs.get("banner", "dice")
        self.banners = kwargs.get("banners", ["dice", "bonobo", "lonewolf"])
        self.title = kwargs.get("title", "Benda")
        self.titles = kwargs.get("titles", ["Benda"])

        # stats
        self.games_played = kwargs.get("games_played", Game.DEFAULT_STATS)
        self.wins = kwargs.get("wins", Game.DEFAULT_STATS)  # fat W's
        self.draws = kwargs.get("draws", Game.DEFAULT_STATS)
        Player._players[id] = self

    @property
    def losses(self):
        """The losses the player has."""
        return {k: self.games_played[k] - self.wins[k] - self.draws[k] for k in self.wins.keys()}

    @property
    def ratio(self):
        """The Win-Loss ratio for the player."""
        ratio_dict = {}
        for k, v in self.wins.items():
            games = v + self.losses[k]
            games = games if games else 1
            ratio_dict[k] = self.wins[k] / games
        return ratio_dict

    @property
    def most_played(self):
        """Returns the most played game."""
        return max(self.games_played, key=self.games_played.get)

    @property
    def user(self):
        return bot.get_user(self.id)

    @classmethod
    def get(cls, id):
        player = cls._players.get(id)
        if not player:
            raise auth.RegistrationError(
                "All players are not registered. Register with the `register` command")
        return player

    ################## STAT MANAGEMENT ##################

    def update(self, game, won=False, draw=False):
        """Update a player."""
        old_xp = self.xp
        self.xp += Game.XP_MULTIPLIERS[game] * Game.XP_VALUES[won]

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
            "banner": self.banner,
            "banners": self.banners,
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
            banner=player.get("banner", "dice"),
            banners=player.get("banners", ["dice", "bonobo", "lonewolf"]),
            title=player.get("title", "Benda"),
            titles=player.get("titles", ["Benda"]),
            games_played=player.get("games_played", Game.DEFAULT_STATS),
            wins=player.get("wins", Game.DEFAULT_STATS),
            draws=player.get("draws", Game.DEFAULT_STATS)
        )

    ################## DRAWING ##################

    def draw_banner(self):
        """Draws the players banner."""
        banner = Image.open(f"assets{sep}banners{sep}{self.banner}.png")
        d = ImageDraw.Draw(banner)  # set image for drawing
        namefnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 47)
        titlefnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 34)
        _, namey = d.textsize(self.name, namefnt)
        name_offset = 100 - namey
        d.text((40, name_offset), self.name, font=namefnt)
        d.text((40, 105), self.title, font=titlefnt)
        return banner

    def draw_xp(self, gains=0):
        """Draws the xp bar"""
        threshold = Player.RANK_THRESHOLD
        # Create new canvas
        xpbar = Image.new(
            mode="RGBA",
            size=(400, 20),
            color=(128, 128, 128, 128)
        )
        d = ImageDraw.Draw(xpbar)  # set image for drawing

        x1, y1 = 0, 0
        gains_percentage = ((self.xp + gains) % threshold)/threshold
        x2 = int(400 * gains_percentage)
        y2 = 20
        d.rectangle((x1, y1, x2, y2), fill=(37, 204, 247, 255))

        xp_percentage = ((self.xp) % threshold) / threshold
        x2 = int(400 * xp_percentage)
        d.rectangle((x1, y1, x2, y2), fill=(24, 44, 97, 255))

        return xpbar

    def draw_card(self, crown=False, gains=0):
        c_width = 420
        c_height = 230

        # Create new canvas
        background = Image.new(
            mode="RGBA",
            size=(c_width, c_height),
            color=(27, 156, 252, 255)
        )

        avatar = drawing.get_user_img(self.user, size=128, mask="circle")
        avatar.thumbnail((100, 100), Image.ANTIALIAS)

        avatar_offset = (10, 10)
        background.paste(avatar, avatar_offset, avatar)

        banner = self.draw_banner()
        banner.thumbnail((400, 100))
        _, bannery = banner.size
        banner_offset = (10, c_height - bannery - 10)
        background.paste(banner, banner_offset)

        xpbar = self.draw_xp(gains=gains)
        xpbar.thumbnail((270, 270))
        xpw, xph = xpbar.size
        xpbar_offset = (c_width - (10 + xpw),
                        c_height - (10 + bannery + 10 + xph))
        background.paste(xpbar, xpbar_offset)

        # Draw winners crown
        if crown:
            crown = Image.open(f"assets{sep}crownicon.png")
            crown.thumbnail((20, 20), Image.ANTIALIAS)
            background.paste(crown, (5, 5), crown)

        return background


class Game:

    _games = {}

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

    def __init__(self, name, channel, *players):
        self.channel = channel
        self.winners = set()
        self.players = list(players)

        self.turn_cycle = islice(cycle(self.players),
                                 randint(0, len(self.players)-1),
                                 None)
        self.lead = next(self.turn_cycle)

        self.name = name
        self.id = channel.id

        Game._games[self.id] = self

    @property
    def ids(self):
        return {p.id for p in self.players}

    @classmethod
    def get(cls, id):
        """Get a game based on a member passed in"""
        return cls._games.get(id)

    def next_turn(self):
        self.lead = next(self.turn_cycle)

    def award_xp(self):
        """Awards all game players XP"""
        for player in self.players:
            player.update(game=self.name,
                          won=player.id in self.winners,
                          draw=not self.winners)

        db.update(*self.players)

    def draw_scoreboard(self):
        """Draw the scoreboard of players"""
        BAR_HEIGHT = 100
        IMGW = 900
        ROWS = len(self.players) + 1
        IMGH = ROWS * BAR_HEIGHT
        PADDING_TOP = .1 * BAR_HEIGHT

        NAME_PCT = .2
        XP_PCT = .6
        RATIO_PCT = .9

        # Make image
        scoreboard = Image.new(
            mode="RGBA",
            size=(IMGW, IMGH),
            color=(0, 0, 0, 0)
        )
        d = ImageDraw.Draw(scoreboard)
        catfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 50)
        statfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 40)

        # draw categories
        for category, pct in zip(("Player", "XP", "W/L"), (NAME_PCT, XP_PCT, RATIO_PCT)):
            msgx, _ = catfnt.getsize(category)
            offset = (pct * IMGW - msgx // 2, PADDING_TOP)
            d.text(offset, category, font=catfnt)

        d.line((0, BAR_HEIGHT, IMGW, BAR_HEIGHT),
               fill=(255, 255, 255, 255), width=5)

        crown = Image.open(f"assets{sep}crownicon.png")
        crown.thumbnail((50, 50), Image.ANTIALIAS)

        for i, player in enumerate(self.players, 1):
            # rem = i % len(self.players) + 1  # 0,1,0,1
            top = BAR_HEIGHT * i
            center = top + BAR_HEIGHT//2

            # DRAW CROWN
            result = player.id in self.winners
            if result:
                _, cy = crown.size
                scoreboard.paste(crown, (10, center - cy//2), crown)

            # DRAW NAME
            msgx, msgy = statfnt.getsize(player.name)
            offset = (NAME_PCT*IMGW - msgx//2,
                      center - msgy//2)
            d.text(offset, player.name, font=statfnt)

            # DRAW XPBAR
            gains = Game.XP_MULTIPLIERS[self.name] * Game.XP_VALUES[result]
            xpbar = player.draw_xp(gains=gains)
            xpbar_width = int(.4 * IMGW)
            xpbar_height = BAR_HEIGHT - 40
            xpbar = xpbar.resize((xpbar_width, xpbar_height))
            xpbar_offset = (int(XP_PCT * IMGW - xpbar_width // 2),
                            center - xpbar_height//2)
            scoreboard.paste(xpbar, xpbar_offset)

            # DRAW W/L RATIO
            ratio = player.ratio[self.name] * 100
            msg = f"{round(ratio, 1)}%"
            msgx, msgy = statfnt.getsize(msg)
            offset = (RATIO_PCT * IMGW - msgx//2,
                      center - msgy//2)
            d.text(offset, msg, font=statfnt)

        return scoreboard

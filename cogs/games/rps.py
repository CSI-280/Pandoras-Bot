"""Module for handling the game of Rock Paper Scissors."""
import random
import discord
from discord.ext import commands
from discord.ext.commands import UserInputError

import drawing
from classes import Game, Player
from auth import authorize
from vars import bot


class RPS(Game):
    """Class for holding the tic tac toe board"""

    def __init__(self, channel, p1, p2):
        super().__init__("rps", channel, p1, p2)

        # Shuffle moves and assign to players
        moves = ["Rock", "Paper", "Scissors"]
        random.shuffle(moves)
        self.p1_moves = {k: v for k, v in enumerate(moves, 1)}
        self.p1_move = None

        random.shuffle(moves)
        self.p2_moves = {k: v for k, v in enumerate(moves, 1)}
        self.p2_move = None

    @property
    def moves(self):
        return {self.p1_move, self.p2_move}

    async def send_dms(self):
        """DM both players with move information."""
        # Player 1 info
        info = ""
        for k, v in self.p1_moves.items():
            info += f"Type **{k}** for **{v}**\n"

        embed = discord.Embed(
            title=f"RPS in #{self.channel.name}", description=info)
        await self.players[0].send(embed=embed)

        # Player 2 info
        if self.players[1].id != bot.user.id:
            info = ""
            for k, v in self.p2_moves.items():
                info += f"Type **{k}** for **{v}**\n"
            embed = discord.Embed(
                title=f"RPS in #{self.channel.name}", description=info)
            await self.players[1].send(embed=embed)

    async def evaluate(self):
        """Evaluate who won the game."""
        if self.players[1].id == bot.user.id:
            self.p2_move = random.choice(("Rock", "Paper", "Scissors"))

        if None in self.moves:
            return

        if len(self.moves) == 1:
            tie_embed = discord.Embed(title="It's a Draw")
            await self.channel.send(embed=tie_embed)
            return await self.end()

        if self.moves == {"Rock", "Paper"}:
            winner = "Paper"
        elif self.moves == {"Scissors", "Paper"}:
            winner = "Scissors"
        elif self.moves == {"Rock", "Scissors"}:
            winner = "Rock"

        # P1 Wins
        if self.p1_move == winner:
            embed = discord.Embed(
                title=f"{self.players[0].name}'s **{winner}** beats {self.players[1].name}'s **{self.p2_move}**")
            await self.channel.send(embed=embed)
            await self.end(winner=self.players[0])

        # P2 Wins
        elif self.p2_move == winner:
            embed = discord.Embed(
                title=f"{self.players[1].name}'s **{winner}** beats {self.players[0].name}'s **{self.p1_move}**")
            await self.channel.send(embed=embed)
            await self.end(winner=self.players[1])

    async def end(self, winner=None, cancelled=False):
        # remove from active games
        game = Game._games.pop(str(self.channel.id) + "rps")

        if cancelled:
            return await game.channel.send(
                f"RPS game between {self.players[0].name} and {self.players[1].name} has been cancelled.")
        elif not winner:
            game.award_xp()
        elif winner:
            game.winners.add(winner.id)
            game.award_xp()

        sb = game.draw_scoreboard()
        await game.channel.send(file=drawing.to_discord_file(sb))


class RockPaperScissorsCog(commands.Cog):
    """Handles all RPS related commands and listeners."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # verify author
        game = Game.get(str(message.channel.id) + "rps")
        if not game or message.author.id not in game.ids:
            return

        if not message.content:
            return

        # end case
        if message.content.lower() == "end":
            await message.delete()
            await game.end(cancelled=True)

        move = message.content[0]  # only first character
        if move not in "123":
            return

        if message.author.id == game.players[0].id and not game.p1_move:
            game.p1_move = game.p1_moves[int(move)]
            await game.evaluate()

        elif message.author.id == game.players[1].id and not game.p2_move:
            game.p2_move = game.p2_moves[int(move)]
            await game.evaluate()

    @commands.command(name="rps", aliases=["rockpaperscissors"])
    async def rock_paper_scissors(self, ctx):
        """Starts up a game of rock paper scissors with another user"""
        authorize(ctx, "mentions")  # check for a mentioned user

        p1 = Player.get(ctx.author.id)
        p2 = Player.get(ctx.message.mentions[0].id)

        # Ensure player is someone else
        if p1 == p2:
            raise UserInputError("You can't play against yourself")

        # Create new game
        embed = discord.Embed(title="Rock Paper Scissors",
                              description=f"{p1.name} **VS** {p2.name}\n\nCheck DMs for how to play")
        await ctx.send(embed=embed)
        game = RPS(ctx.channel, p1, p2)
        await game.send_dms()


def setup(bot):
    bot.add_cog(RockPaperScissorsCog(bot))

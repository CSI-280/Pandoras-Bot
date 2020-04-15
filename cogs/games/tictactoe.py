"""Module for handling the game of tic tac toe."""
import io
import random
from os.path import sep
import asyncio
from itertools import cycle

import discord
import requests
from discord.ext import commands
from discord.ext.commands import UserInputError
from PIL import Image, ImageDraw, ImageFont, ImageOps

import drawing
from auth import authorize
from classes import Player, Game
from vars import bot, get_help, get_prefix


class TicTacToe(Game):
    """Class for holding the tic tac toe board"""

    def __init__(self, channel, p1, p2):
        super().__init__("tictactoe", channel, p1, p2)

        # choose a random starting player
        self.active_player = random.choice((p1, p2))
        self.versus_msg = None
        self.board_msg = None

        self.board = {k: None for k in range(9)}

    @property
    def ids(self):
        return {p.id for p in self.players}

    def draw_board(self, **kwargs):
        """Draw the tic-tac-toe board."""
        canvas_width = 800
        midpoint = canvas_width // 6  # 133

        # Create new canvas
        background = Image.open(f"assets{sep}TicTacToeBoard.png")
        d = ImageDraw.Draw(background)  # set image for drawing

        # fonts
        bigfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 200)
        smallfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 72)

        # draw the message at the bottom of the image
        if kwargs.get("footer"):
            d.text((40, canvas_width), kwargs.get("footer"),
                   font=smallfnt, fill=(255, 255, 255, 255))
        else:
            background = background.crop((0, 0, canvas_width, 800))
            d = ImageDraw.Draw(background)  # set image for drawing

            # Draw board values or numbers
        for k, v in self.board.items():

            # The board is split into 6 sections x and y in order to center things easier
            div = (k // 3) * 2 + 1  # 1, 1, 1, 3, 3, 3, 5, 5, 5 ---> Y Values
            rem = (k % 3) * 2 + 1  # 1, 3, 5 repeating X Values

            text_color = (255, 255, 255, 20)
            # Convert player to X and O
            if v:
                v = "X" if v == self.players[0] else "O"
                text_color = (255, 255, 255, 255)

            # generate message and offset values
            msg = str(k) if not v else v
            msgx, msgy = d.textsize(msg, bigfnt)
            msg_offset = (msgx/2, msgy/2)

            # Draw numbers in grid cells
            x = midpoint * rem - msg_offset[0]
            y = midpoint * div - msg_offset[1] - 20
            d.text((x, y), msg, font=bigfnt, fill=text_color)

        # Draw the winner line
        if kwargs.get("winner"):
            winfo = kwargs.get("winner")
            draw_pos = (
                ((winfo["start"] % 3) * 2+1) * midpoint,  # x1
                ((winfo["start"] // 3) * 2+1) * midpoint,  # y1
                ((winfo["end"] % 3) * 2+1) * midpoint,  # x2
                ((winfo["end"] // 3) * 2+1) * midpoint  # y2
            )
            d.line(draw_pos, fill=(255, 0, 0, 255), width=15)

        return background

    async def update(self):
        """Update game statistics"""
        # switch whose turn it is
        self.end_turn()

        new_board = self.draw_board(footer=f"{self.lead.name}'s turn")
        new_board = drawing.to_discord_file(new_board)

        if self.board_msg:
            await self.board_msg.delete()

        self.board_msg = await self.channel.send(file=new_board)

        # CPU player not smart for now
        # if self.p2 == bot.user:
        #     options = [x for x in range(9) if not self.board[x]]
        #     move = random.choice(options)
        #     await asyncio.sleep(1)
        #     await self.channel.send(content=str(move), delete_after=0)

    def check_win(self):
        """Check if the board has a winner."""
        b = self.board

        # check rows
        for i in range(0, 7, 3):
            if b[i] == b[i+1] == b[i+2] and b[i]:
                return {"winner": b[i], "start": i, "end": i+2}

        # Check columns
        for i in range(3):
            if b[i] == b[i+3] == b[i+6] and b[i]:
                return {"winner": b[i], "start": i, "end": i+6}

        # Check Diagonals
        if b[0] == b[4] == b[8] and b[0]:
            return {"winner": b[0], "start": 0, "end": 8}

        if b[2] == b[4] == b[6] and b[2]:
            return {"winner": b[2], "start": 2, "end": 6}

    async def end(self, *args, winfo=None):
        """End the game and clean up"""

        # remove from active games
        game = Game._games.pop(self.channel.id)

        # update the board with win line if applicable
        if game.board_msg:
            await game.board_msg.delete()

        # set what the bot draws
        if winfo:
            winner = winfo["winner"]
            board = game.draw_board(winner=winfo)
            game.winners.add(winner=winner.id)
            game.award_xp()
        elif "tie" in args:
            board = game.draw_board(footer="It's a tie!")
            game.award_xp()
        else:
            board = game.draw_board(footer="Game Cancelled")
            return

        await game.channel.send(file=drawing.to_discord_file(board))


class TicTacToeCog(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # verify author
        game = Game.get(message.channel.id)
        if not game or message.author.id not in [p.id for p in game.players]:
            return

        if message.content == "":
            return

        # end case
        if message.content.lower() == "end":
            await message.delete()
            await game.end(cancel=True)

        move = message.content[0:1]  # only first character

        # check that space is open and input is valid
        if message.author == game.active_player and move in "012345678":
            # verify move available
            if not game.board[int(move)]:
                await message.delete()
                game.board[int(move)] = game.lead
                winfo = game.check_win()

                # winner
                if winfo:
                    await game.end(winner=winfo)

                # board is full
                elif all(game.board.values()):
                    await game.end("tie")

                # continue playing
                else:
                    await game.update()

    @commands.command(name="tictactoe", aliases=["ttt", "t"])
    async def tictactoe(self, ctx):
        """Starts up a game of tic tac toe with another user"""
        authorize(ctx, "mentions")  # check for a mentioned user

        p1 = Player.get(ctx.author.id)
        p2 = Player.get(ctx.message.mentions[0].id)

        if p1 == p2:
            raise UserInputError("Can't play against yourself")

        # Create new game
        game = TicTacToe(ctx.channel, p1, p2)

        # draw and send versus
        file = drawing.to_discord_file(drawing.draw_versus(p1.user, p2.user))
        await game.channel.send(file=file)

        # draw and send board
        await game.update()


def setup(bot):
    bot.add_cog(TicTacToeCog(bot))

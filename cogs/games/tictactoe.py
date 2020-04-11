"""Module for handling the game of tic tac toe."""
import io
import random
from os.path import sep

import discord
from discord.ext import commands
from discord.ext.commands import UserInputError
from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
import drawing

from vars import bot, get_prefix, get_help
from auth import authorize


class Game:
    """Class for holding the tic tac toe board"""
    _games = {}  # all of the active games

    def __init__(self, p1, p2, channel):
        self.p1 = p1
        self.p2 = p2

        # choose a random starting player
        self.active_player = random.choice((p1, p2))
        self.channel = channel
        self.id = self.channel.id
        self.versus_msg = None
        self.board_msg = None

        Game._games[self.id] = self
        self.board = {k: None for k in range(9)}

    @property
    def players(self):
        return (self.p1, self.p2)

    @staticmethod
    def get(id):
        """Get a game based on a member passed in"""
        return Game._games.get(id)

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
                v = "X" if v == self.p1 else "O"
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
        self.active_player = self.p1 if self.active_player == self.p2 else self.p2

        new_board = self.draw_board(footer=f"{self.active_player.name}'s turn")
        new_board = drawing.to_discord_file(new_board)

        if self.board_msg:
            await self.board_msg.delete()

        self.board_msg = await self.channel.send(file=new_board)

        # CPU player not smart for now
        if self.p2 == bot.user:
            options = [x for x in range(9) if not self.board[x]]
            move = random.choice(options)
            await self.channel.send(content=str(move), delete_after=0)

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

    async def end(self, **results):
        """End the game and clean up"""

        # remove from active games
        game = Game._games.pop(self.channel.id)

        # update the board with win line if applicable
        await game.board_msg.delete()

        # set what the bot draws
        if results.get("winner"):
            board = game.draw_board(winner=results.get("winner"))
        elif results.get("tie"):
            board = game.draw_board("It's a tie!")
        else:
            board = game.draw_board("Game Cancelled")

        await game.channel.send(file=drawing.to_discord_file(board))

        # count turns and generate stats
        turns = list(game.board.values()).count(None) + 1
        stats = {
            "XP": "+40",
        }

        # draw and send winner image
        winfo = results.get("winner")
        win_image = drawing.draw_winner(winfo["winner"], **stats)
        file = drawing.to_discord_file(win_image, name="winner")
        await game.channel.send(file=file)


class TicTacToe(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # verify author
        game = Game.get(message.channel.id)
        if not game or message.author not in game.players:
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
                game.board[int(move)] = game.active_player
                win_info = game.check_win()

                # winner
                if win_info:
                    await game.end(winner=win_info)

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

        p1 = ctx.author
        p2 = ctx.message.mentions[0]  # first mentioned user

        if p1 == p2:
            raise UserInputError("Can't play against yourself")

        # Create new game
        game = Game(p1, p2, ctx.channel)

        # draw and send versus
        file = drawing.to_discord_file(drawing.draw_versus(p1, p2))
        game.versus_msg = await game.channel.send(file=file)

        # draw and send board
        await game.update()


def setup(bot):
    bot.add_cog(TicTacToe(bot))

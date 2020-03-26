"""Module for handling the game of tic tac toe."""
import io
import random
from os.path import sep

import discord
from discord.ext import commands
from discord.ext.commands import UserInputError
from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests

from vars import bot, get_prefix, get_help, tictactoe_q
from auth import authorize


class Game:
    """Class for holding the tic tac toe board"""
    _games = {}  # all of the active games

    def __init__(self, p1, p2, channel):
        self.p1 = p1
        self.p2 = p2
        self.turn = random.choice((p1, p2))  # choose a random starting player
        self.channel = channel
        self.versus_msg = None
        self.board_msg = None

        Game._games[self.id] = self
        Game._games[Game.mkid(p2)] = self

        # We will have to develop a better way than this for battleship
        self.board = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None
        }

    @property
    def id(self):
        return int(str(self.p1.id) + str(self.p1.guild.id))

    @staticmethod
    def get(member):
        """Get a game based on a member passed in"""
        return Game._games.get(Game.mkid(member))

    def draw_board(self, footer, win_coords=None):
        """Draw the tic-tac-toe board."""
        canvas_width = 800

        midpoint = canvas_width // 6  # 133

        # Create new canvas
        background = Image.open(f"assets{sep}TicTacToeBoard.png")
        d = ImageDraw.Draw(background)  # set image for drawing

        # fonts
        bigfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 200)
        smallfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 72)

        # draw whos turn it is
        d.text((40, canvas_width), footer,
               font=smallfnt, fill=(255, 255, 255, 255))

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
        if win_coords:
            draw_pos = (
                ((win_coords[0] % 3) * 2+1) * midpoint,  # x1
                ((win_coords[0] // 3) * 2+1) * midpoint,  # y1
                ((win_coords[1] % 3) * 2+1) * midpoint,  # x2
                ((win_coords[1] // 3) * 2+1) * midpoint  # y2
            )
            d.line(draw_pos, fill=(255, 0, 0, 255), width=15)

            # return byte array to send
        byte_arr = io.BytesIO()
        background.save(byte_arr, format="webp")
        return io.BytesIO(byte_arr.getvalue())

    def draw_versus(self):
        """Draws a versus image to start the match"""
        canvas_width = 537
        canvas_height = 300

        # Create new canvas
        background = Image.new(
            mode="RGBA",
            size=(canvas_width, canvas_height),
            color=(0, 0, 0, 0)
        )

        d = ImageDraw.Draw(background)  # set image for drawing
        fnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 30)

        # load versus
        versus = Image.open(f"assets{sep}RedVersus.png")
        versus.thumbnail((192, 192), Image.ANTIALIAS)

        # get discord pfps
        url = self.p1.avatar_url_as(static_format="webp", size=256)
        response = requests.get(url)
        avatar1 = Image.open(io.BytesIO(response.content))

        url = self.p2.avatar_url_as(static_format="webp", size=256)
        response = requests.get(url)
        avatar2 = Image.open(io.BytesIO(response.content))

        # Draw Circular Mask
        masksize = (256, 256)
        mask = Image.new('L', masksize, 0)  # Black/White
        maskdraw = ImageDraw.Draw(mask)
        maskdraw.ellipse((0, 0) + masksize, fill=255)

        # cut circles out of pfps
        avatar1 = ImageOps.fit(avatar1, mask.size, centering=(0.5, 0.5))
        avatar1.putalpha(mask)
        avatar2 = ImageOps.fit(avatar2, mask.size, centering=(0.5, 0.5))
        avatar2.putalpha(mask)

        # Calculate offsets
        versus_offset = (canvas_width//2 - versus.size[0]//2,
                         128-versus.size[1]//2)
        avatar2_offset = (canvas_width - avatar2.size[0] + 0, 0)

        # paste images on background
        background.paste(avatar1, (0, 0), avatar1)
        background.paste(avatar2, avatar2_offset, avatar2)
        background.paste(versus, versus_offset, versus)

        # Draw names
        name1width, _ = d.textsize(self.p1.name, fnt)
        name2width, _ = d.textsize(self.p2.name, fnt)
        name1pos = (128 - name1width/2, 266)
        name2pos = ((canvas_width-128) - name2width/2, 266)
        d.text(name1pos, self.p1.name, font=fnt, fill=(255, 255, 255, 255))
        d.text(name2pos, self.p2.name, font=fnt, fill=(255, 255, 255, 255))

        # return byte array to send
        byte_arr = io.BytesIO()
        background.save(byte_arr, format="webp")
        return io.BytesIO(byte_arr.getvalue())

    async def update(self):
        """Update game statistics"""
        # switch whose turn it is
        self.turn = self.p1 if self.turn == self.p2 else self.p2
        new_board = discord.File(fp=self.draw_board(f"{self.turn.name}'s turn'"),
                                 filename="board.webp")
        await self.board_msg.delete()
        self.board_msg = await self.channel.send(file=new_board)

    def check_win(self):
        """Check if the board has a winner"""
        b = self.board

        # check rows
        for i in range(0, 7, 3):
            if b[i] == b[i+1] == b[i+2] and b[i]:
                return b[i], (i, i+2)

        # Check columns
        for i in range(3):
            if b[i] == b[i+3] == b[i+6] and b[i]:
                return b[i], (i, i+6)

        # Check Diagonals
        if b[0] == b[4] == b[8] and b[0]:
            return b[0], (0, 8)

        if b[2] == b[4] == b[6] and b[2]:
            return b[2], (2, 6)

    async def end(self, winner=None):
        """End the game and clean up"""
        p1id = Game.mkid(self.p1)
        p2id = Game.mkid(self.p2)
        tictactoe_q.difference_update({self.p1.id, self.p2.id})
        Game._games.pop(p1id)
        game = Game._games.pop(p2id)

        if not winner:
            msg = "Game Cancelled"
            win_coords = None
        elif winner == "Nobody":
            msg = "It's a tie!"
            win_coords = None
        else:
            msg = f"{winner[0].name} wins!"
            win_coords = winner[1]

        await game.board_msg.delete()
        file = discord.File(fp=game.draw_board(msg, win_coords),
                            filename="board.webp")
        await game.channel.send(file=file)

    @staticmethod
    def mkid(player):
        """Generates a gameid given a player."""
        return int(str(player.id) + str(player.guild.id))


class TicTacToe(commands.Cog):
    """Handles all of the simple commands such as saying howdy or
    the help command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id not in tictactoe_q:
            return

        if message.content == "":
            return

        game = Game.get(message.author)
        move = message.content[0:1]

        # end case
        if message.content.lower() == "end":
            await message.delete()
            await game.end()

        # check that space is open and input is valid
        if message.author == game.turn and move in "012345678":
            if not game.board[int(move)]:
                await message.delete()
                game.board[int(move)] = game.turn
                winner = game.check_win()
                if winner:
                    await game.end(winner)
                elif not winner and all(game.board.values()):
                    await game.end("Nobody")
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

        tictactoe_q.update({p1.id, p2.id})

        # Create new game
        game = Game(p1, p2, ctx.channel)
        file = discord.File(fp=game.draw_versus(), filename="versus.webp")
        game.versus_msg = await game.channel.send(file=file)
        file = discord.File(fp=game.draw_board(f"{game.turn.name}'s turn"),
                            filename="board.webp")
        game.board_msg = await game.channel.send(file=file)


def setup(bot):
    bot.add_cog(TicTacToe(bot))

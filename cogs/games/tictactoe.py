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
        self.board_msg = None
        self.board = {k: None for k in range(9)}

    def draw_board(self, *args, **kwargs):
        """Draw the tic-tac-toe board."""

        # Create new canvas
        background = Image.open(f"assets{sep}TicTacToeBoard.png")
        d = ImageDraw.Draw(background)  # set image for drawing

        IMGW, IMGH = background.size
        MID = IMGW // 6  # The dist to middle of each column/row

        # fonts
        bigfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 240)
        smallfnt = ImageFont.truetype(f"assets{sep}Roboto.ttf", 72)

        # draw the message at the bottom of the image
        if kwargs.get("footer"):
            d.text((40, IMGH-100), kwargs.get("footer"),
                   font=smallfnt, fill=(255, 255, 255, 255))
        else:
            # crop 100 px off the bottom
            background = background.crop((0, 0, IMGW, IMGH-100))
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
                msg = v
            else:
                msg = str(k)

            # generate message offset values
            msgx, msgy = bigfnt.getsize(msg)

            # Draw numbers in grid cells
            x = MID * rem - (msgx//2)
            y = MID * div - (msgy//2) - 25
            d.text((x, y), msg, font=bigfnt, fill=text_color)

        # Draw the winner line
        if "winner" in kwargs:
            winfo = kwargs.get("winner")
            draw_pos = (
                ((winfo["start"] % 3) * 2+1) * MID,  # x1
                ((winfo["start"] // 3) * 2+1) * MID,  # y1
                ((winfo["end"] % 3) * 2+1) * MID,  # x2
                ((winfo["end"] // 3) * 2+1) * MID  # y2
            )
            d.line(draw_pos, fill=(255, 0, 0, 255), width=15)

        if "draw" in args:
            dx, dy = bigfnt.getsize("DRAW!")
            draw_offset = (IMGW//2 - dx//2, IMGH//2 - dy//2)
            d.text(draw_offset, "DRAW!", font=bigfnt, fill=(235, 77, 75, 255))

        return background

    async def update(self):
        """Update game statistics"""
        # switch whose turn it is
        self.next_turn()

        # Have the bot move
        if self.lead.id == bot.user.id and not all(self.board.values()):
            self.automove()
            self.next_turn()

        # Check win
        winfo = self.check_win()
        if winfo:
            return await self.end("winner")
        elif all(self.board.values()):
            return await self.end("draw")

        new_board = self.draw_board(footer=f"{self.lead.name}'s turn")
        new_board = drawing.to_discord_file(new_board)

        try:
            await self.board_msg.delete()
        except:
            pass

        self.board_msg = await self.channel.send(file=new_board)

    def check_win(self):
        """Check if the board has a winner."""
        b = self.board

        # check Rows
        for i in range(0, 7, 3):
            if b[i] == b[i+1] == b[i+2] and b[i]:
                return {"winner": b[i], "start": i, "end": i+2}

        # Check Columns
        for i in range(3):
            if b[i] == b[i+3] == b[i+6] and b[i]:
                return {"winner": b[i], "start": i, "end": i+6}

        # Check Diagonals
        if b[0] == b[4] == b[8] and b[0]:
            return {"winner": b[0], "start": 0, "end": 8}

        if b[2] == b[4] == b[6] and b[2]:
            return {"winner": b[2], "start": 2, "end": 6}

    def check_potential_win(self):
        """Checks to see if a player can win and provides the move to block or win"""
        b = self.board

        bpl = []  # bot-prioritized list
        for player in self.players:
            if player.id == bot.user.id:
                bpl.insert(0, player)
            else:
                bpl.append(player)

        for player in bpl:
            # check Rows
            for i in range(0, 7, 3):
                count = 0
                empty = i
                for j in range(3):
                    if b[i+j] == player:
                        count += 1
                    else:
                        empty = i + j
                if count >= 2 and not b[empty]:
                    return empty

            # Check Columns
            for i in range(3):
                count = 0
                empty = i
                for j in range(0, 7, 3):
                    if b[i+j] == player:
                        count += 1
                    else:
                        empty = i + j
                if count >= 2 and not b[empty]:
                    return empty

            # Check Diagonals
            count = 0
            empty = i
            for i in range(0, 9, 4):
                if b[i] == player:
                    count += 1
                else:
                    empty = i
            if count >= 2 and not b[empty]:
                return empty

            count = 0
            empty = i
            for i in range(2, 7, 2):
                if b[i] == player:
                    count += 1
                else:
                    empty = i
            if count >= 2 and not b[empty]:
                return empty
        return 4

    async def end(self, *args):
        """End the game and clean up"""

        # remove from active games
        game = Game._games.pop(self.channel.id)

        # update the board with win line if applicable
        if game.board_msg:
            await game.board_msg.delete()

        # set what the bot draws

        if "winner" in args:
            winfo = game.check_win()
            winner = winfo["winner"]
            board = game.draw_board(winner=winfo)
            game.winners.add(winner.id)
            game.award_xp()
        elif "draw" in args:
            board = game.draw_board("draw")
            game.award_xp()
        else:
            board = game.draw_board(footer="Game Cancelled")

        await game.channel.send(file=drawing.to_discord_file(board))

        if "winner" in args or "tie" in args:
            sb = game.draw_scoreboard()
            await game.channel.send(file=drawing.to_discord_file(sb))

    def automove(self):
        """Automatically chooses a move for the lead player"""
        edges = (self.board[1], self.board[3], self.board[5], self.board[7])
        options = [x for x in range(9) if not self.board[x]]  # open spots

        if not self.board[4]:
            move = 4

        # move on side if middle taken
        elif len(options) == 8 and self.board[4]:
            move = random.choice((0, 2, 6, 8))

        elif len(options) == 7 and any(edges):
            move = 8 if self.board[1] or self.board[3] else 0

        elif len(options) == 6:
            if self.board[1] and self.board[3]:
                move = 0
            elif self.board[1] and self.board[5]:
                move = 2
            elif self.board[3] and self.board[7]:
                move = 6
            elif self.board[5] and self.board[7]:
                move = 8
            else:
                move = 4
        else:
            # check for wins
            move = self.check_potential_win()

        if self.board[move]:
            move = random.choice(options)
        self.board[move] = self.lead


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
        if not game or message.author.id not in game.ids:
            return

        if message.content == "":
            return

        # end case
        if message.content.lower() == "end":
            await message.delete()
            await game.end()

        move = message.content[0:1]  # only first character

        # check that space is open and input is valid
        if message.author.id == game.lead.id and move in "012345678":
            # verify move available
            if not game.board[int(move)]:
                await message.delete()
                game.board[int(move)] = game.lead
                await game.update()

    @commands.command(name="tictactoe", aliases=["ttt", "t"])
    async def tictactoe(self, ctx):
        """Starts up a game of tic tac toe with another user"""
        authorize(ctx, "mentions")  # check for a mentioned user

        p1 = Player.get(ctx.author.id)
        p2 = Player.get(ctx.message.mentions[0].id)

        if p1 == p2:
            raise UserInputError("You can't play against yourself")

        # Create new game
        game = TicTacToe(ctx.channel, p1, p2)

        # draw and send board
        await game.update()


def setup(bot):
    bot.add_cog(TicTacToeCog(bot))

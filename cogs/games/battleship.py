import discord
from discord.ext import commands
import random
import os


class BattleShip:
    def print_board(s, board):

        # find out if you are printing the user 1 or 2 board
        player = "user 2"
        if s == "u":
            player = "User 1"

        print("The " + player + "'s board look like this: \n")

        # print the horizontal numbers
        print(" ")
        for i in range(10):
            print("  " + str(i + 1) + "  ")
        print("\n")

        for i in range(10):

            # print the vertical line number
            if i != 9:
                print(str(i + 1) + "  ")
            else:
                print(str(i + 1) + " ")

            # print the board values, and cell dividers
            for j in range(10):
                if board[i][j] == -1:
                    print(' ')
                elif s == "u":
                    print(board[i][j])
                elif s == "c":
                    if board[i][j] == "*" or board[i][j] == "$":
                        print(board[i][j])
                    else:
                        print(" ")

                if j != 9:
                    print(" | ")
            print

            # print a horizontal line
            if i != 9:
                print("   ----------------------------------------------------------")
            else:
                print

    def place_ships(self, board, ships):
        # Place the user's ships and validate location.

    def place_ship(self, board, ship, s, ori, x, y):
        # Place the ship at the correct orientation(vertical or horizontal)

    def validate(self, board, ship, x, y, ori):
        # Validate that the ship can be placed at given coordinates.

    def v_or_h(self):
        # While true, ask the user if they want their ship placed vertically or horizontally.

    def get_coor(self):
        # While true, ask the user for the coordinates they wish to attack at.

    def make_move(self, board,x,y):
        # Make a move on the board and return the result, hit, miss or try again for repeat hit.

    def user_move(self, board):
        # Get coordinates from the user and try to make move.
        # If move is a hit, check ship sunk and win condition.

    def check_sink(self, board, x, y):
        # Check which kind of ship is hit, mark the coordinate as a hit, then check if ship is sunk.

    def check_win(self, board):
        # Check the board to see if win condition is met. If there's a char that isn't hit or miss, return false.

def main():
    # Create the ship types, board, player boards, and game loop.

if __name__ == "__main__":
    main()

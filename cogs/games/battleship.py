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
        for ship in ships.keys():

            # get coordinates from user and validate the postion
            valid = False
            while (not valid):

                self.print_board("u", board)
                print("Placing a/an ") + ship
                x, y = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(board, ships[ship], x, y, ori)
                if not valid:
                    print("Cannot place a ship there.\nPlease take a look at the board and try again.")
                    input("Hit ENTER to continue")

            # place the ship
            board = self.place_ship(board, ships[ship], ship[0], ori, x, y)
            self.print_board("u", board)

        input("Done placing user ships. Hit ENTER to continue")
        return board

    def place_ships_user_2(self, board, ships):
        # Place the second user's ships and validate location.
        for ship in ships.keys():

            # get coordinates from user and validate the postion
            valid = False
            while (not valid):

                self.print_board("s", board)
                print("Placing a/an ") + ship
                x, y = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(board, ships[ship], x, y, ori)
                if not valid:
                    print("Cannot place a ship there.\nPlease take a look at the board and try again.")
                    input("Hit ENTER to continue")

            # place the ship
            board = self.place_ship(board, ships[ship], ship[0], ori, x, y)
            self.print_board("u", board)

        input("Done placing user ships. Hit ENTER to continue")
        return board

    def place_ship(self, board, ship, s, ori, x, y):
        # Place the ship at the correct orientation(vertical or horizontal)
        if ori == "v":
            for i in range(ship):
                board[x + i][y] = s
        elif ori == "h":
            for i in range(ship):
                board[x][y + i] = s

        return board

    def validate(self, board, ship, x, y, ori):
        # Validate that the ship can be placed at given coordinates.
        if ori == "v" and x + ship > 10:
            return False
        elif ori == "h" and y + ship > 10:
            return False
        else:
            if ori == "v":
                for i in range(ship):
                    if board[x + i][y] != -1:
                        return False
            elif ori == "h":
                for i in range(ship):
                    if board[x][y + i] != -1:
                        return False

        return True
    
    def v_or_h(self):
        # While true, ask the user if they want their ship placed vertically or horizontally.

        user_oritentation = ""
        invalid_input = True

        while invalid_input is True:

            # Prompt the user for an input
            user_input = input(
                "Enter either h or v for your ships direction (horizontal or vertical): ")

            # Vertical Ship Placement
            if user_input == "v":
                print("\nShip will be placed vertically")
                invalid_input = False

            # Horizontal ship placement
            elif user_input == "h":
                print("\nShip will be placed horizontally")
                invalid_input = False

            # User Input was neither horizontal nor vertical
            else:
                print("Input was invalid, please try again (enter h or v)\n")
                invalid_input = True

        # If the input was either h or v return ship orientation
        if not invalid_input:
            user_oritentation = user_input

        return user_oritentation


    def get_coor(self):
        # While true, ask the user for the coordinates they wish to attack at.

        user_coordinates = ()
        confirmation = ""

        # While loop to check if the coordinates are what the user actually wants
        while confirmation != "y":

            # While loop to check if the x coordinate is valid
            while True:
                # Check the x coordinate
                try:
                    # See if it's an integer
                    x = int(input(
                        "Enter the x coordinate you'd like to place a ship or attack at (between 0-9): "))
                except ValueError:
                    print("ERROR: Input is not a number")
                else:
                    # See if it's between 0-9, if it is move on to the y coord.
                    if 0 <= x <= 9:
                        break
                    else:
                        print("ERROR: Number is not in range, try again")
                        continue
            # While loop to check if the y coordinate is valid
            while True:

                # Check the y coordinate
                try:
                    # Check if it's an integer
                    y = int(input(
                        "Enter the y coordinate you'd like to place a ship or attack at (between 0-9): "))
                except ValueError:
                    print("ERROR: Input is not a number")
                else:
                    # See if it's between 0-9, if it is confirm this is the coord. the user wants
                    if 0 <= y <= 9:
                        break
                    else:
                        print("ERROR: Number is not in range, try again")
                        continue

            print(f"You chose coordinates {(x, y)} is this the correct position?")

            confirmation = input("\nEnter either y or n: ")

            # If yes, then it is the coord. that the player desires
            if confirmation == "y":
                user_coordinates = (x, y)
                print(f"\nConfirmed coordinated for {user_coordinates}")
                break

            # If no, then the player didn't put the correct coord. in, and should try again
            elif confirmation == "n":
                print("Incorrect coordinates, try again\n")
                continue

            # If the input is neither yes or no, try again until valid input
            while confirmation != "y" or confirmation != "n":
                print("This is not a valid option, try again")
                confirmation = input("Enter y or n: ")

                if confirmation == "y":
                    user_coordinates = (x, y)
                    print(f"\nConfirmed coordinated for {user_coordinates}")
                    break

                elif confirmation == "n":
                    print("Incorrect coordinates, try again\n")
                    break

        # Return the confirmed coordinates
        return user_coordinates

    def make_move(self, board,x,y):
        # Make a move on the board and return the result, hit, miss or try again for repeat hit.
        print("")

    def user_move(self, board):
        # Get coordinates from the user and try to make move.
        # If move is a hit, check ship sunk and win condition.
        print("")

    def check_sink(self, board, x, y):
        # Check which kind of ship is hit, mark the coordinate as a hit, then check if ship is sunk.
        print("")

    def check_win(self, board):
        # Check the board to see if win condition is met. If there's a char that isn't hit or miss, return false.
        print("")


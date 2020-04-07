import discord

from vars import bot

# async def user_join(member):
#     """Open player data and write new data for level system."""
#     with open('users.json', 'r') as f:
#         users = json.load(f)

#     # Make an await command for updating the data.

#     # Write the new data.
#     with open('users.json', 'w') as f:
#         json.dump(users, f)


# async def on_win(player):
#     """Add experience to the winner of a game"""
#     with open('users.json', 'r') as f:
#         users = json.load(f)

#     # Make an await command for updating the data, adding experience, and leveling up.
#     # Specify the amount of xp to give the user.

#     # Write the new data.
#     with open('users.json', 'w') as f:
#         json.dump(users, f)


async def update_data(users, user):
    """Add new users if they don't already exist and set default xp and level along with their name."""


async def add_experience(users, user, xp):
    """Add the specified amount of xp."""


async def level_up(users, user, channel):
    """Check to see if a user leveled up and update if true"""

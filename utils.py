
from classes import Player

import database as db


def award_xp(*player_ids, game=None, winner=None):
    if not game:
        return

    updated_players = []
    for id in player_ids:
        player = Player.get(id)
        updated_players.append(player)
        player.update(game, won=player.id == winner, draw=not winner)

    db.update(*updated_players)

from ticTacToe.errors import InputException


def is_players_valid(players: str):
    if not players or not 0 < len(players.split(",")) < 3:
        raise InputException("only a one or two players can play")


def is_another_game_valid(another_game: str):
    if another_game not in {'y', 'n'}:
        raise InputException("please enter one of y or n")

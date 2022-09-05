from ticTacToe.errors import InputException

"""
the general input validations functions
"""


def is_players_valid(players: str):
    """
    validate that the amount of players is between 1 and 2
    """
    if not players or not 0 < len(players.split(",")) < 3:
        raise InputException("only a one or two players can play")


def is_another_game_valid(another_game: str):
    """
    validate that the input is enum of y or n
    """
    if another_game not in {'y', 'n'}:
        raise InputException("please enter one of y or n")

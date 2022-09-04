import random

from ticTacToe.board_handler import BoardHandler
from ticTacToe.utils import get_input
from ticTacToe.utils import get_symbols_env

SYMBOLS = get_symbols_env()


class Player:
    """
    The players modals.
    those modals represent the base player; every player must contain a name, symbol and score.
    """

    def __init__(self, name: str, symbol: str):
        self.name: str = name
        self.symbol: str = symbol
        self.score = 0

    def select_next_move(self, game_handler) -> int:
        pass

    def add_win(self):
        """
        in case of a win increase the player score by 2
        """
        self.score += 2

    def add_tie(self):
        """
        in case of a tie increase the player score by 1
        """
        self.score += 1


class HumanPlayer(Player):
    """
    a Human player is an extension of the base player class, the difference is in the selection of the move method;
    a human player will have select next move method that allows him to choose the next spot he wishes to play
    """

    def __init__(self, name: str, symbol: str):
        super().__init__(name=name, symbol=symbol)

    def select_next_move(self, game_handler) -> int:
        """
        print the board and get the next move from the player
        :param game_handler: the game handler class to display the score during the game selection using
                showScores command
        """
        print(f'{self.name}, select where would you like to place "{self.symbol}"')
        print(game_handler.board_handler)
        return int(get_input(
            input_text="Enter spot: ",
            validation_func=game_handler.board_handler.is_spot_valid,
            game_handler=game_handler
        ))


class ComputerPlayer(Player):
    """
    a Computer player is an extension of the base player class, the difference is in the selection of the move method;
    a computer player will have select next move method that will calculate the best move available on the board
    and return it.
    """

    def __init__(self, symbol):
        super().__init__(name="The best tic-tac-toe computer", symbol=symbol)

    def select_next_move(self, game_handler) -> int:
        """
        compute and return the best move on the board
        :param game_handler: the game handler to get the best move on the game board
        """
        spot: int = game_handler.board_handler.compute_next_best_move_minimax(self.symbol)
        print(f'{self.name}, selected spot {spot}"')
        return spot

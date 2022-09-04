from ticTacToe.utils import get_input

"""
The players modals.
those modals represent the players every player must contain a name, symbol and score.
there are to different types of players:
    a. human normal Player
    b. computer player
a human player will have select next move method that allows him to chose the next spot he want to play
a computer player will have select next move method that will calculate the best move available and return it.
"""


class Player:
    def __init__(self, name: str, symbol: str):
        self.name: str = name
        self.symbol: str = symbol
        self.score = 0

    def select_next_move(self, game_handler) -> int:
        pass

    def add_win(self):
        self.score += 2

    def add_tie(self):
        self.score += 1


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str):
        super().__init__(name=name, symbol=symbol)

    def select_next_move(self, game_handler) -> int:
        print(f'{self.name}, select where would you like to place "{self.symbol}"')
        print(game_handler.board_handler)
        return int(get_input(
            input_text="Enter spot: ",
            validation_func=game_handler.board_handler.is_spot_valid,
            game_handler=game_handler
        ))


class ComputerPlayer(Player):
    def __init__(self, symbol):
        super().__init__(name="The best tic-tac-toe computer", symbol=symbol)

    def select_next_move(self, game_handler) -> int:
        spot: int = game_handler.board_handler.compute_next_best_move(self.symbol)
        print(f'{self.name}, selected spot {spot}"')
        return spot

from ticTacToe.utils import get_input
from ticTacToe.board_handler import BoardHandler


class Player:
    def __init__(self, name: str, symbol: str):
        self.name: str = name
        self.symbol: str = symbol
        self.score = 0

    def select_next_move(self, board_handler: BoardHandler):
        print(f'{self.name}, select where would you like to place "{self.symbol}"')
        print(board_handler)
        return get_input(
            input_text="Enter spot: ",
            validation_func=board_handler.is_spot_valid
        )


class Computer(Player):
    def __init__(self, symbol):
        super().__init__(name="The best tic-tac-toe computer", symbol=symbol)

    def select_next_move(self, board_handler: BoardHandler):
        pass

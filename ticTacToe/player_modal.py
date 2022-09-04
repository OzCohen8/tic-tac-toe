from ticTacToe.utils import get_input


# todo fix the import issue
class Player:
    def __init__(self, name: str, symbol: str):
        self.name: str = name
        self.symbol: str = symbol
        self.score = 0

    def select_next_move(self, game_handler) -> int:
        print(f'{self.name}, select where would you like to place "{self.symbol}"')
        print(game_handler.board_handler)
        return int(get_input(
            input_text="Enter spot: ",
            validation_func=game_handler.board_handler.is_spot_valid,
            game_handler=game_handler
        ))

    def add_win(self):
        self.score += 2

    def add_tie(self):
        self.score += 1


class Computer(Player):
    def __init__(self, symbol):
        super().__init__(name="The best tic-tac-toe computer", symbol=symbol)

    def select_next_move(self, game_handler) -> int:
        spot: int = game_handler.board_handler.compute_next_best_move(self.symbol)
        print(f'{self.name}, selected spot {spot}"')
        return spot

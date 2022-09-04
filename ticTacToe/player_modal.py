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
        board_handler: BoardHandler = game_handler.board_handler
        if len(board_handler.get_empty_spots()) == 9:
            return random.randint(1, 9)

        spot: int = self.minimax(board_handler)
        print(f'{self.name}, selected spot {spot}"')
        return spot

    def minimax(self, board_handler: BoardHandler, player, depth: int):
        max_player = self.symbol  # yourself
        opponent_symbol = SYMBOLS[0] if player != SYMBOLS[0] else SYMBOLS[1]

        # first we want to check if the previous move is a winner
        if state.current_winner == opponent_symbol:
            return {'position': None, 'score': 1 * (depth + 1) if opponent_symbol == max_player else
            -1 * (depth + 1)}
        elif not board_handler.is_empty_spots_left():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': float("-inf")}  # each score should maximize
        else:
            best = {'position': None, 'score': float("inf")}  # each score should minimize

        for possible_move in board_handler.get_empty_spots():
            if board_handler.select_board_spot_and_check_winner(possible_move, player)
            sim_score = self.minimax(board_handler, opponent_symbol)  # simulate a game after making that move

            # undo move
            board_handler.undo_spot_selection(possible_move)
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

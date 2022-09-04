import random
from typing import List, Dict
import numpy as np
from termcolor import colored

from ticTacToe.errors import InputException
from ticTacToe.utils import get_symbols_env

minimax_score: Dict[str, int] = {
    "X": 1,
    "O": -1,
    "tie": 0
}


class BoardHandler:
    """
    The Board handler is the interface which presents the game board.
    this class is responsible for all the board logic and functionalities.
    Board workflow:
    1. new game started- new board need to be created.
    2. in every player move, first a validation is required to check if the spot is free and the input is correct.
    3. then the move is preformed and the board handler checks if there is a winner or a tie.
    Board logic:
    1. the data-type chosen to represent the board is numpy array
       (could be a dict too I wanted to make it a bit mor interesting :) ).
    2. every board position element is represented by a number from 1 to 9 to simplify the spot selections to the player.
    3. the player symbols are abstract to the board class and saved as there negative ascii because:
        3.1 numpy handles better ints then strings,
        3.2 they are saved as theirs negative values
            so in case that will be needed to handle a bigger board the number would never appear as a spot.
    """

    def __init__(self, board_size: int):
        """
        creating a new clean tic-tac-toe board
        Args:
            board_size: the board raw and column size ( in our case 3 ) -> for more abstract class
            board: if we want to create a board handler class based on existing board,
                   we use this functionality in the process of computing the best next move for our computer player
            available_spots: same as the board args-> the available spots of the existing board
        """
        self.board_size = board_size
        self.board = None
        self.reset_board()

    def __is_there_winner(self, last_spot_raw: int, last_spot_column: int, last_symbol__negative_ascii: int) -> int:
        """
        checks if the current board state contains a winner.
        Args:
            last_spot_raw: the last selected spot raw
            last_spot_column: the last selected spot column
            last_symbol__negative_ascii: the last spot player symbol
        """
        # check win at the raw entered
        if np.all(self.board[last_spot_raw] == last_symbol__negative_ascii):
            return True
        # check win at the column entered
        trans_arr = self.board.T
        if np.all(trans_arr[last_spot_column] == last_symbol__negative_ascii):
            return True
        # check win at the diagonals
        if np.all(self.board.diagonal() == last_symbol__negative_ascii):
            return True
        if np.all(np.diag(np.fliplr(self.board)) == last_symbol__negative_ascii):
            return True
        return False

    def __minimax(self, depth: int, is_maximizing: bool) -> int:
        resualt = self.__is_there_winner()
        if resualt:
            return minimax_score[resualt]
        if is_maximizing:
            best_score = float("-inf")
            for spot in self.available_spots:
                # set board with spot
                score = self.__minimax(depth+1, False)
                # remove the move from board
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for spot in self.available_spots:
                # set board with spot
                score = self.__minimax(depth+1, True)
                # remove the move from board
                best_score = min(score, best_score)
            return best_score

    def undo_spot_selection(self, spot):
        raw: int = (spot-1) // 3
        column: int = (spot-1) % 3
        self.board[raw, column] = spot

    def get_empty_spots(self):
        return np.transpose(np.nonzero(self.board > 0))

    def is_spot_valid(self, spot: str) -> None:
        """
        validate the selected spot input.
        Args:
            spot: the selected spot by the player
        """
        if spot not in {str(x) for x in range(1, 10)}:
            raise InputException(f"spot {spot} is not valid choice!")
        spot = int(spot)
        raw: int = (spot-1) // 3
        column: int = (spot-1) % 3
        if self.board[raw, column] < 0:
            raise InputException(f"spot {spot} is already taken!")

    def is_empty_spots_left(self):
        """
        checks if the board is full (no more empty spots left)
        """
        return np.amax(self.board) > 0

    def select_board_spot_and_check_winner(self, spot: int, symbol: str) -> int:
        """
        select the spot on the board and checks for a winner
        Args:
            spot: the selected spot
            symbol: the player symbol which we need the spot to be
        Returns:
            1 - if there is a winner
            2 - if the game is tied
            0 - if the game is still ongoing (0 is false as boolean which be easier to interact on the game handler)
        """
        raw: int = (spot-1) // 3
        column: int = (spot-1) % 3
        symbol_negative_ascii: int = -ord(symbol)
        self.board[raw, column] = symbol_negative_ascii
        if self.__is_there_winner(raw, column, symbol_negative_ascii):
            return 1
        if not self.is_empty_spots_left():
            return 2
        return 0

    def compute_next_best_move_minimax(self, my_symbol: str):
        max_player = my_symbol  # yourself
        best_score = float("-inf")
        best_spot = None

        symbols = get_symbols_env()
        opponent_symbol = symbols[0] if my_symbol != symbols[0] else symbols[1]

        for spot in self.__get_empty_spots():
            # set board with spot
            score = self.__minimax(0, True)
            # remove the move from board
            self.__undo_spot_selection(spot)
            if score > best_score:
                best_score = score
                best_spot = spot
        return best_spot

    def reset_board(self):
        """
        clear the board and available spots for new game
        """
        self.board = np.arange(1, self.board_size**2 + 1).reshape(self.board_size, self.board_size)

    def __str__(self):
        board_str: str = "  -     -     -  \n"
        for raw in range(3):
            for col in range(3):
                current_spot = self.board[raw][col]
                if current_spot < 0:
                    current_spot = colored(chr(current_spot * -1), "green")
                board_str += f"  {current_spot}  " if col != 1 else f"|  {current_spot}  |"
            board_str += "\n  -     -     -  \n"
        return board_str

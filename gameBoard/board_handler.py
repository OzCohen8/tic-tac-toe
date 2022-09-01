import numpy as np
import random
from gameBoard.errors import InputException
from termcolor import colored
from typing import Tuple
"""
Board logic:
a. the data-type chosen to represent the board is numpy array.
b. every board position element is represented by 0 1 or -1 ->
    0- no one selected,
    1- player one selected (ie X),
    -1- player two selected (ie )
"""


class BoardHandler:
    def __init__(self, board_size: int):
        """
        creating a new clean tic-tac-toe board
        """
        self.board_size = board_size
        self.board = None
        self.available_spots = set()
        self.reset_board()

    def __is_there_winner(self, last_spot_raw: int, last_spot_column: int, last_symbol__negative_ascii: int) -> bool:
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

    # def __compute_next_best_move(self):
    #     if len(self.available_spots) == 9:
    #         spot = random.randint(1, 9)
    #     elif len(self.available_spots) == 8 and 5 in self.available_spots:
    #         spot = 5
    #     elif

    def is_spot_valid(self, spot: str) -> None:
        if spot not in set([str(x) for x in range(1, 10)]):
            raise InputException(f"spot {spot} is not valid choice!")
        spot = int(spot)
        if spot not in self.available_spots:
            raise InputException(f"spot {spot} is already taken!")
        self.available_spots.remove(spot)

    def is_empty_spots_left(self):
        return len(self.available_spots) > 0

    def select_board_spot_and_check_winner(self, spot: str, symbol: str) -> bool:
        raw: int = (int(spot)-1) // 3
        column: int = (int(spot)-1) % 3
        symbol_negative_ascii: int = -ord(symbol)
        self.board[raw, column] = symbol_negative_ascii
        return self.__is_there_winner(raw, column, symbol_negative_ascii)

    def reset_board(self):
        self.board = np.arange(1, self.board_size**2 + 1).reshape(self.board_size, self.board_size)
        self.available_spots = {num for num in range(1, self.board_size**2 + 1)}

    def __str__(self):
        board_str: str = "  -     -     -  \n"
        for r in range(3):
            for c in range(3):
                current_spot = self.board[r][c]
                if current_spot < 0:
                    current_spot = colored(chr(current_spot * -1), "green")
                board_str += f"  {current_spot}  " if c != 1 else f"|  {current_spot}  |"
            board_str += "\n  -     -     -  \n"
        return board_str


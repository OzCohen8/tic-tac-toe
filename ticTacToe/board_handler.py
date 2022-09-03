import random
from typing import List

import numpy as np
from ticTacToe.errors import InputException
from termcolor import colored

"""
Board logic:
a. the data-type chosen to represent the board is numpy array.
b. every board position element is represented by 0 1 or -1 ->
    0- no one selected,
    1- player one selected (ie X),
    -1- player two selected (ie )
"""


class BoardHandler:
    def __init__(self, board_size: int, board=None, available_spots=None):
        """
        creating a new clean tic-tac-toe board
        """
        self.board_size = board_size
        if board is not None and available_spots:
            self.board = board
            self.available_spots = available_spots
        else:
            self.board = None
            self.available_spots = set()
            self.reset_board()

    def __is_there_winner(self, last_spot_raw: int, last_spot_column: int, last_symbol__negative_ascii: int, board=None) -> bool:
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

    def __copy_board_handler(self):
        return BoardHandler(self.board_size, np.copy(self.board), self.available_spots.copy())

    def is_spot_valid(self, spot: str) -> None:
        if spot not in set([str(x) for x in range(1, 10)]):
            raise InputException(f"spot {spot} is not valid choice!")
        spot = int(spot)
        if spot not in self.available_spots:
            raise InputException(f"spot {spot} is already taken!")

    def is_empty_spots_left(self):
        return len(self.available_spots) > 0

    def select_board_spot_and_check_winner(self, spot: int, symbol: str) -> bool:
        raw: int = (spot-1) // 3
        column: int = (spot-1) % 3
        symbol_negative_ascii: int = -ord(symbol)
        self.board[raw, column] = symbol_negative_ascii
        self.available_spots.remove(spot)
        return self.__is_there_winner(raw, column, symbol_negative_ascii)

    def compute_next_best_move(self) -> int:
        available_spots = self.available_spots

        # todo: make generics symbols
        # Check for possible winning move to take or to block opponents winning move
        for symbol in ['O', 'X']:
            for spot in available_spots:
                next_board_handler: BoardHandler = self.__copy_board_handler()
                if next_board_handler.select_board_spot_and_check_winner(spot, symbol):
                    return spot

        # Try to take one of the corners
        open_corners: List[int] = []
        for spot in available_spots:
            if spot in [1, 3, 7, 9]:
                open_corners.append(spot)
        if len(open_corners) > 0:
            return random.choice(open_corners)

        # Try to take the center
        if 5 in available_spots:
            return 5

        # Take any edge
        for spot in available_spots:
            return spot

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

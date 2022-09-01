import numpy as np
from gameBoard.errors import SpotException
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
    def __init__(self):
        """
        creating a new clean tic-tac-toe board
        """
        self.board = None
        self.available_spots = set()
        self.reset_board()

    def __is_spot_valid(self, spot: str) -> None:
        if spot not in set([str(x) for x in range(1, 10)]):
            raise SpotException(f"spot {spot} is not valid choice!")
        if spot not in self.available_spots:
            raise SpotException(f"spot {spot} is already taken!")
        self.available_spots.remove(spot)

    def __is_there_winner(self, last_spot_raw: int, last_spot_column: int, last_symbol: str) -> bool:
        is_raw_winner: bool = True
        is_column_winner: bool = True
        is_corner: bool = True

        for i in range(3):
            if self.board[last_spot_raw, i] != last_symbol:
                is_raw_winner = False
            if self.board[i, last_spot_column] != last_symbol:
                is_column_winner = False
        return is_column_winner or is_raw_winner

    def is_empty_spots_left(self):
        return len(self.available_spots) > 0

    def select_board_spot_and_check_winner(self, spot: str, symbol: str) -> bool:
        self.__is_spot_valid(spot)
        raw: int = (int(spot)-1) // 3
        column: int = (int(spot)-1) % 3
        self.board[raw, column] = symbol
        return self.__is_there_winner(raw, column, symbol)

    def reset_board(self):
        self.board = np.array([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], np.str)
        self.available_spots = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

    def __str__(self):
        board_str: str = "  -     -     -  \n"
        for r in range(3):
            for c in range(3):
                board_str += f"  {self.board[r][c]}  " if c != 1 else f"|  {self.board[r][c]}  |"
            board_str += "\n  -     -     -  \n"
        return board_str



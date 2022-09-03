import random
from typing import List
import numpy as np
from termcolor import colored

from ticTacToe.errors import InputException

"""
The Board handler is the interface which presents the game board.
this class is responsible for all the board logic and functionalities.
Board workflow:
1. new game started- new board need to be created.
2. in every player move, first a validation is required to check if the spot is free and the input is correct.
3. then the move is preformed and the board handler checks if there is a winner or a tie.
Board logic:
1. the data-type chosen to represent the board is numpy array (could be a dict too I wanted to make it a bit mor interesting :) ).
2. every board position element is represented by a number from 1 to 9 to simplify the spot selections to the end user (player).
3. the player symbols are abstract to the board class and saved as there negative ascii because:
    3.1 numpy handles better ints then strings,
    3.2 they are saved as theirs negative values so in case that will be needed to handle a bigger board the number would never appeare as a spot.
"""


class BoardHandler:
    def __init__(self, board_size: int, board=None, available_spots=None):
        """
        creating a new clean tic-tac-toe board
        Args:
            board_size: the board raw and column size ( in our case 3 ) -> for more abstract class
            board: if we want to create a board handler class based on existing board,
                   we use this functionality in the process of computing the best next move for our computer player
            available_spots: same as the board args-> the available spots of the existing board
        """
        self.board_size = board_size
        if board is not None and available_spots:
            self.board = board
            self.available_spots = available_spots
        else:
            self.board = None
            self.available_spots = set()
            self.reset_board()

    def __is_there_winner(self, last_spot_raw: int, last_spot_column: int, last_symbol__negative_ascii: int) -> bool:
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

    def __copy_board_handler(self):
        return BoardHandler(self.board_size, np.copy(self.board), self.available_spots.copy())

    def is_spot_valid(self, spot: str) -> None:
        """
        validate the selected spot input.
        Args:
            spot: the selected spot by the player
        """
        if spot not in set([str(x) for x in range(1, 10)]):
            raise InputException(f"spot {spot} is not valid choice!")
        spot = int(spot)
        if spot not in self.available_spots:
            raise InputException(f"spot {spot} is already taken!")

    def is_empty_spots_left(self):
        return len(self.available_spots) > 0

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
        self.available_spots.remove(spot)
        if self.__is_there_winner(raw, column, symbol_negative_ascii):
            return 1
        elif not self.is_empty_spots_left():
            return 2
        return 0

    def compute_next_best_move(self, my_symbol: str) -> int:
        """
        compute and find the best possible move on the board
        strategy:
            1. in case only one move made select the center
            2. check if there is a move that is a winner or to block opponent
            3. if two opposite corners spots are of the opponent, and I have the middle mark an edge
            4. check if the corners are empty if they are select them
            5. go for the middle
            6. at last take the edges
        Args:
            my_symbol: the computer symbol
        """

        if len(self.available_spots) == 9:
            return random.randint(1, 9)

        if len(self.available_spots) == 8 and 5 in self.available_spots:
            return 5

        # todo: make generics symbols && need to check first my symbol
        # todo omprove alg and add minmax alg stage 6
        # Check for possible winning move to take or to block opponents winning move
        for symbol in [my_symbol, "X"]:
            for spot in self.available_spots:
                next_board_handler: BoardHandler = self.__copy_board_handler()
                if next_board_handler.select_board_spot_and_check_winner(spot, symbol):
                    return spot

        if len(self.available_spots) == 6:
            # if two opposite corners spots are of the opponent, and I have the middle mark an edge
            if self.board[0, 0] == self.board[2, 2] or self.board[0,2] == self.board[2,0]:
                return 2
            elif self.board[0, 0] < 0:
                return 9
            elif self.board[2, 2] < 0:
                return 1
            elif self.board[0, 2] < 0:
                return 7
            elif self.board[2, 0]:
                return 3

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
        """
        clear the board and available spots for new game
        """
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

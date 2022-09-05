import random
from typing import Tuple
import numpy as np
from termcolor import colored
from ticTacToe.utils import config_parameters
from ticTacToe.errors import InputException


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
        self.board_size: int = board_size
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

    def __convert_spot_raw_column(self, spot: int) -> Tuple[int, int]:
        raw: int = (spot-1) // self.board_size
        column: int = (spot-1) % self.board_size
        return raw, column

    def __is_empty_spots_left(self) -> bool:
        """
        checks if the board is full (no more empty spots left)
        """
        return np.amax(self.board) > 0

    def __get_empty_spots(self):
        return np.transpose(np.nonzero(self.board > 0))

    def __minimax(self, maximizing_player_symbol: str, player_symbol, depth: int = 9):
        opponent_symbol = config_parameters["SYMBOL_A"] if player_symbol != config_parameters["SYMBOL_A"] else config_parameters["SYMBOL_B"]

        if player_symbol == maximizing_player_symbol:
            best_move = {'spot': None, 'score': float("-inf")}  # each score should maximize
        else:
            best_move = {'spot': None, 'score': float("inf")}  # each score should minimize

        for possible_move in self.__get_empty_spots():
            possible_move = possible_move[0]*3 + possible_move[1] + 1
            result: int = self.select_board_spot_and_check_winner(possible_move, player_symbol)
            if result == 1:
                self.undo_spot_selection(possible_move)
                return {'spot': possible_move, 'score': 1 * (depth + 1) if player_symbol == maximizing_player_symbol else
                -1 * (depth + 1)}
            elif result == 2:
                self.undo_spot_selection(possible_move)
                return {'spot': possible_move, 'score': 0}

            score = self.__minimax(maximizing_player_symbol, opponent_symbol, depth-1)  # simulate a game after making that move

            # undo move
            self.undo_spot_selection(possible_move)
            score['spot'] = possible_move  # this represents the move optimal next move

            if player_symbol == maximizing_player_symbol:  # X is max player
                if score['score'] > best_move['score']:
                    best_move = score
            elif score['score'] < best_move['score']:
                best_move = score
        return best_move

    def undo_spot_selection(self, spot) -> None:
        raw, column = self.__convert_spot_raw_column(spot)
        self.board[raw, column] = spot

    def is_spot_valid(self, spot: str) -> None:
        """
        validate the selected spot input.
        Args:
            spot: the selected spot by the player
        """
        if spot not in {str(x) for x in range(1, self.board_size**2 + 1)}:
            raise InputException(f"spot {spot} is not valid choice!")
        spot = int(spot)
        raw, column = self.__convert_spot_raw_column(spot)
        if self.board[raw, column] < 0:
            raise InputException(f"spot {spot} is already taken!")

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
        raw, column = self.__convert_spot_raw_column(spot)
        symbol_negative_ascii: int = -ord(symbol)
        self.board[raw, column] = symbol_negative_ascii
        if self.__is_there_winner(raw, column, symbol_negative_ascii):
            return 1
        if not self.__is_empty_spots_left():
            return 2
        return 0

    def compute_next_best_move(self, my_symbol: str):
        if len(self.__get_empty_spots()) == self.board_size**2:
            return random.randint(1, self.board_size**2)
        return self.__minimax(my_symbol, my_symbol)["spot"]

    def reset_board(self):
        """
        clear the board and available spots for new game
        """
        self.board = np.arange(1, self.board_size**2 + 1).reshape(self.board_size, self.board_size)

    def __str__(self):
        seperate_raw: str = "".join(["  -  " for i in range(self.board_size)])
        board_str: str = f"{seperate_raw}\n"
        for raw in range(self.board_size):
            for col in range(self.board_size):
                current_spot = self.board[raw][col]
                if current_spot < 0:
                    player_symbol = chr(current_spot * -1)
                    color: str = "green" if player_symbol == config_parameters["SYMBOL_A"] else "blue"
                    current_spot = colored(player_symbol, color)
                board_str += f"  {current_spot}  " if col == 0 else f"|  {current_spot}  "
            board_str += f"\n{seperate_raw}\n"
        return board_str

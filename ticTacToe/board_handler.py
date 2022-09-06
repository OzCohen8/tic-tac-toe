import random
from typing import Tuple, List
import numpy as np
from termcolor import colored
from ticTacToe.utils import config_parameters, convert_spot_row_column
from ticTacToe.errors import InputException


class BoardHandler:
    """
    The Board handler is the interface which presents the game board.
    his responsibilities mainly include; the board logic and functionalities.
    Board workflow:
    1. new game started-new board need to be created.
    2. after player move, first a validation is required to check if the spot is free and the input is correct.
    3. then the move is preformed and the board handler checks if the move resulted a win or a tie.
    Board logic:
    1. the data-type chosen to represent the board is numpy array
       (could be a dict or a list too I wanted to make it a bit mor interesting :) ).
    2. every board position element is represented by a number from 1 to n**2 (n is row length)
      to simplify the spot selections to the player.
    3. the player symbols are abstract to the board class and saved as there negative ascii because:
        3.1 numpy handles better ints then strings,
        3.2 they are saved as theirs negative values
            so in case that will be needed to handle a bigger board the number would never appear as a spot.
    """

    def __init__(self, board_size: int):
        """
        creating a new clean tic-tac-toe board
        Args:
            board_size: the board row and column size ( in our case 3 ) -> for more abstract class
        """
        self.board_size: int = board_size
        self.board = None
        self.reset_board()

    def __is_there_winner(self, last_row: int, last_column: int, last_symbol__negative_ascii: int) -> int:
        """
        checks if the current board state contains a winner.
        Args:
            last_spot_row: the last selected spot row
            last_spot_column: the last selected spot column
            last_symbol__negative_ascii: the last spot player symbol
        """
        # check win at the row entered
        if np.all(self.board[last_row] == last_symbol__negative_ascii):
            return True
        # check win at the column entered
        trans_arr = self.board.T
        if np.all(trans_arr[last_column] == last_symbol__negative_ascii):
            return True
        # check win at the diagonals
        if np.all(self.board.diagonal() == last_symbol__negative_ascii):
            return True
        if np.all(np.diag(np.fliplr(self.board)) == last_symbol__negative_ascii):
            return True
        return False

    def __is_empty_spots_left(self) -> bool:
        """
        checks if the board is full (no more empty spots left)
        """
        return np.amax(self.board) > 0

    def __get_empty_spots(self):
        """
        get all empty spots
        :return: an array containing row, column of every spot
        """
        return np.transpose(np.nonzero(self.board > 0))

    def __minimax(self, maximizing_player_symbol: str, player_symbol, depth: int = 9):
        """
        the minimax algorithm. used in our case to calc the best available move on the board.
        Args:
            maximizing_player_symbol: the symbol of the computer player (should win)
            player_symbol: the current players turn symbol
            depth: keeps track how far are we in the minimax alg
        """
        opponent_symbol = config_parameters["SYMBOL_A"] if player_symbol != config_parameters["SYMBOL_A"] else config_parameters["SYMBOL_B"]

        if player_symbol == maximizing_player_symbol:
            best_move = {'spot': None, 'score': float("-inf")}  # if it's the computer we are searching for the max score
        else:
            best_move = {'spot': None, 'score': float("inf")}  # if it's  not the computer we are searching for the min score (negative)

        for possible_move in self.__get_empty_spots():
            row, col = possible_move[0], possible_move[1]
            result: int = self.select_board_spot_and_check_winner(row, col, player_symbol)
            if result == 1:
                self.__undo_spot_selection(row, col)
                return {
                    'spot': possible_move,
                    'score': 1 * (depth + 1) if player_symbol == maximizing_player_symbol else -1 * (depth + 1)
                }
            elif result == 2:
                self.__undo_spot_selection(row, col)
                return {'spot': possible_move, 'score': 0}

            score = self.__minimax(maximizing_player_symbol, opponent_symbol, depth-1)  # simulate a game after making that move

            # undo move
            self.__undo_spot_selection(row, col)
            # setting the spot which maybe better than the old best one
            score['spot'] = possible_move

            if player_symbol == maximizing_player_symbol:
                if score['score'] > best_move['score']:
                    best_move = score
            elif score['score'] < best_move['score']:
                best_move = score
        return best_move

    def __undo_spot_selection(self, spot_row: int, spot_col: int) -> None:
        """
        roll back a move on the board
        Args:
            spot_row: the spot row to roll-back from
            spot_col: the spot column to roll-back from
        """
        self.board[spot_row, spot_col] = (spot_col+1) + (spot_row*3)

    def is_spot_valid(self, spot: str) -> None:
        """
        validate the selected spot input.
        Args:
            spot: the selected spot by the player
        """
        if spot not in {str(x) for x in range(1, self.board_size**2 + 1)}:
            raise InputException(f"spot {spot} is not valid choice!")
        spot = int(spot)
        row, column = convert_spot_row_column(spot)
        if self.board[row, column] < 0:
            raise InputException(f"spot {spot} is already taken!")

    def select_board_spot_and_check_winner(self, row: int, col: int, symbol: str) -> int:
        """
        select the spot on the board and checks for a winner
        Args:
            row: the row of the selected spot
            col: the column of the selected spot
            symbol: the player symbol which we need the spot to be
        Returns:
            1 - if there is a winner
            2 - if the game is tied
            0 - if the game is still ongoing (0 is false as boolean which be easier to interact on the game handler)
        """
        symbol_negative_ascii: int = -ord(symbol)
        self.board[row, col] = symbol_negative_ascii
        if self.__is_there_winner(row, col, symbol_negative_ascii):
            return 1
        if not self.__is_empty_spots_left():
            return 2
        return 0

    def compute_next_best_move(self, my_symbol: str) -> Tuple[int, int]:
        """
        calculate the next best move for the player,
        in case of the first move select a spot randomly
        Args:
            my_symbol: the player symbol
        """
        if len(self.__get_empty_spots()) == self.board_size**2:
            return random.randint(0, self.board_size-1), random.randint(0, self.board_size-1)
        return self.__minimax(my_symbol, my_symbol)["spot"]

    def compute_next_best_move_conditions(self, my_symbol: str) -> Tuple[int, int]:
        """
        it is possible also to calc the next best move following those conditions

        compute and find the best possible move on the board
        strategy:
            1. in case only one move made select the center
            2. check if there is a move that is a winner or to block opponent
            3. if two opposite corners spots are of the opponent, and I have the middle mark an edge
            4. if exactly 3 plays where made, and I am in the center
               place next move in the corner which is in the same row/column as the opponents moves
            4. check if the corners are empty if they are select them
            5. go for the middle
            6. at last take the edges
        Args:
            my_symbol: the computer symbol
        """
        pass

    def reset_board(self):
        """
        clear the board and available spots for new game
        """
        self.board = np.arange(1, self.board_size**2 + 1).reshape(self.board_size, self.board_size)

    def __str__(self):
        separate_row: str = "".join(["  -   " for i in range(self.board_size)])
        board_str: str = f"{separate_row}\n"
        for row in range(self.board_size):
            for col in range(self.board_size):
                current_spot = self.board[row][col]
                if current_spot < 0:
                    player_symbol = chr(current_spot * -1)
                    color: str = "green" if player_symbol == config_parameters["SYMBOL_A"] else "blue"
                    current_spot = colored(player_symbol, color)
                board_str += f"  {current_spot}  " if col == 0 else f"|  {current_spot}  "
            board_str += f"\n{separate_row}\n"
        return board_str




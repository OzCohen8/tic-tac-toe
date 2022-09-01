from typing import Dict, List, Any
import random

from gameBoard.vaidators import *
from gameBoard.board_handler import BoardHandler
from gameBoard.utils import get_input
from gameBoard.player_modal import Player, Computer


class GameHandler:
    def __init__(self):
        self.players: Dict[int, Player] = {}
        self.board_handler: BoardHandler = BoardHandler(board_size=3)

    def __set_players(self, players: List[str]):
        player1: Player = Player(name=players[0].strip(), symbol="X")
        if len(players) > 1:
            player2: Player = Player(name=players[1].strip(), symbol="O")
        else:
            player2: Computer = Computer(symbol="O")
        self.players = {1: player1, -1: player2}
        print(f'Welcome {player1.name} and {player2.name} lets start\n'
              f'{player1.name} you will be "{player1.symbol}"'
              f' and {player2.name} will be "{player2.symbol}"')

    @staticmethod
    def __roll_who_start():
        return random.choice([1, -1])

    def start_game(self) -> int:
        self.board_handler.reset_board()
        current_turn = self.__roll_who_start()
        print(f'{self.players[current_turn].name} you will start!')
        while not self.play_turn_and_check_winner(current_turn):
            if not self.board_handler.is_empty_spots_left():
                print("Its a Tie Game")
                return 0
            current_turn *= -1
        print(f"{self.players[current_turn].name} Wins!!!")
        return current_turn

    def start_games(self):
        while True:
            game_result: int = self.start_game()
            if game_result in self.players:
                self.players[game_result].score += 2
            else:
                self.players[1].score += 1
                self.players[-1].score += 1
            another_game: str = get_input(
                input_text="Want to play another game? (y/n): ",
                validation_func=is_another_game_valid
            )
            if another_game == 'n':
                print("Player {} won with score of: {}")
                break

    def play_turn_and_check_winner(self, current_turn: int) -> bool:
        turn_symbol: str = self.players[current_turn].symbol
        spot: str = self.players[current_turn].select_next_move(self.board_handler)
        return self.board_handler.select_board_spot_and_check_winner(spot, turn_symbol)

    def run_game(self):
        """
        this function gets and sets the players, starts the game,
        """
        print("Welcome to Oz's tic-tac-toe game!\nplease enter the players names, (can be one player or two :) )")
        players: str = get_input(
            input_text="Enter players names: ",
            validation_func=is_players_valid
        )
        self.__set_players(players.split(","))
        self.start_games()

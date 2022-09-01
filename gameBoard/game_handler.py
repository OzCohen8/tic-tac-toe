from typing import Dict, List
import random

from gameBoard.board_handler import BoardHandler
from gameBoard.errors import SpotException
from gameBoard.player_modal import Player


class GameHandler:
    def __init__(self, player1: str, player2: str = None):
        player1: Player = Player(name=player1, symbol="X")
        player2: Player = Player(
            name=player2 if player2 else "The best tic-tac-toe computer",
            symbol="O"
        )
        print(f'Welcome {player1.name} and {player2.name} lets start\n'
              f'{player1.name} you will be "{player1.symbol}"'
              f' and {player2.name} will be "{player2.symbol}"')
        self.players: Dict[int, Player] = {1: player1, -1: player2}
        self.board_handler: BoardHandler = BoardHandler()

    def __roll_who_start(self):
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
            print("Want to play another game? (y/n)")
            another_game: str = ""
            while True:
                another_game = input("Enter: ")
                if another_game in {'n', 'y'}:
                    break
                print("not a valid input should be one of y or n")
            if another_game == 'n':
                print("Player {} won with score of: {}")
                break

    def play_turn_and_check_winner(self, current_turn: int) -> bool:
        turn_symbol: str = self.players[current_turn].symbol
        print(f'{self.players[current_turn].name}, select where would you like to place "{turn_symbol}"')
        print(self.board_handler)
        while True:
            try:
                spot = input("Enter: ")
                return self.board_handler.select_board_spot_and_check_winner(spot, turn_symbol)
            except SpotException as e:
                print(e)

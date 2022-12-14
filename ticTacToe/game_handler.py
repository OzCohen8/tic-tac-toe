from typing import Dict, List
import random
from termcolor import colored

from ticTacToe.vaidators import *
from ticTacToe.board_handler import BoardHandler
from ticTacToe.utils import get_input, config_parameters
from ticTacToe.players_modals import Player, HumanPlayer, ComputerPlayer


class GameHandler:
    """
    The Game handler is the interface which handles the game workflow.
    this class is responsible for setting the players, running the games and count the score.

    some logic:
    the track on the players turns is implemented by indexing (via a dict) the players with 1 and -1 as keys,
    it makes the turn pattern really easy; it is just needed to multiply the turn flag by -1 to move to next player
    """

    def __init__(self):
        self.__players: Dict[int, Player] = {}
        self.board_handler: BoardHandler = BoardHandler(config_parameters["BOARD_ROW_SIZE"])

    def __set_players(self, players: List[str]) -> None:
        """
        responsible for creating the players instances, if there is only one player a computer player should be created.
        Args:
            players: list contains the players names.
        """
        player1: HumanPlayer = HumanPlayer(name=players[0].strip(), symbol=config_parameters["SYMBOL_A"])
        if len(players) > 1:
            player2: HumanPlayer = HumanPlayer(name=players[1].strip(), symbol=config_parameters["SYMBOL_B"])
        else:
            player2: ComputerPlayer = ComputerPlayer(symbol=config_parameters["SYMBOL_B"])
        self.__players = {1: player1, -1: player2}
        print(f'\nWelcome {player1.name} and {player2.name} lets start\n'
              f'{player1.name} you will be "{player1.symbol}"'
              f' and {player2.name} will be "{player2.symbol}"')
        print("Note that anytime during the games you can enter showScores to see the score\n")

    @staticmethod
    def __roll_who_start():
        return random.choice([1, -1])

    def __run_one_game(self) -> None:
        """
        a function which is responsible on the workflow of a single game
        """
        # reset the board from last game
        self.board_handler.reset_board()
        current_turn = self.__roll_who_start()
        print(f'{self.__players[current_turn].name} you will start!')
        turn_result: int = self.__play_turn_and_check_winner(current_turn)
        while not turn_result:
            current_turn *= -1
            turn_result = self.__play_turn_and_check_winner(current_turn)

        print(self.board_handler)
        # add the score of the game to the players
        if turn_result == 2:
            for player in self.__players.values():
                player.add_score(config_parameters["TIE_POINTS"])
            print("Its a Tie Game")
        else:
            self.__players[current_turn].add_score(config_parameters["WIN_POINTS"])
            print(f"{self.__players[current_turn].name} Wins!!!")

    def __play_turn_and_check_winner(self, current_turn: int) -> int:
        """
        play the turn on the board and check if the move resulted a win\tie
        Args:
            current_turn: 1 or -1 indicates which player turn
        Returns:
            1 - if there is a winner
            2 - if the game is tied
            0 - if the game is still ongoing (0 is false as boolean which be easier to interact with)
        """
        turn_symbol: str = self.__players[current_turn].symbol
        row, col = self.__players[current_turn].select_next_move(self)
        return self.board_handler.select_board_spot_and_check_winner(row, col, turn_symbol)

    def __get_winner(self):
        """
        gets the player with the bigger score if score are equal returns False
        """
        players: List[Player] = list(self.__players.values())
        if players[0].score == players[1].score:
            return False
        return players[0] if players[0].score > players[1].score else players[1]

    def show_scores(self):
        """
        a method to print the current game score
        """
        players = list(self.__players.values())
        score_str: str = f"{players[0].name}-{colored(players[0].score, 'green')}"
        score_str += f" VS {colored(players[1].score, 'blue')}-{players[1].name}"
        print(f"The Game Score: {score_str}")

    def run_games(self):
        """
        the run function; first gets the players as input set them and run the games until the user wishes to quit
        """
        print('''Welcome to Oz's tic-tac-toe game!\nplease enter the players names seperated by ",", (can be one player or two :) )''')
        players: str = get_input(
            input_text="Enter players names: ",
            validation_func=is_players_valid
        )
        self.__set_players(players.split(","))
        while True:
            self.__run_one_game()
            another_game: str = get_input(
                input_text="Want to play another game? (y/n): ",
                validation_func=is_another_game_valid,
                game_handler=self
            )
            if another_game == 'n':
                winner = self.__get_winner()
                if winner:
                    print(f"{winner.name} won with score of: {winner.score}")
                else:
                    print("Its a Tie game!!")
                break

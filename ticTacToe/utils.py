from typing import Any
import os

from dotenv import load_dotenv
from ticTacToe.errors import InputException

"""
common use function across the tic-tac-toe module
"""

load_dotenv()


def get_input(input_text: str, validation_func, game_handler=None) -> Any:
    """
    generic function to get input from the player, validate it, in case the input is not valid asks for the input again
    :param input_text: the text that will be presented to the user while asking for the input
    :param validation_func: the validation which need to check against that input
    :param game_handler: (optional) the game state handler for the ability to show score any time the program ask for input
    :return: the input params
    """
    while True:
        input_args = input(input_text)
        try:
            validation_func(input_args)
            return input_args
        except InputException as e:
            if input_args.strip() == "showScores" and game_handler:
                game_handler.show_scores()
            else:
                print("Input exception; " + str(e))


def get_symbols_env(symbols=None):
    """"
    get the symbols from the .env file
    :param symbols: (optional) default symbols to use if the env file is not accessible
    """
    symbols = symbols if symbols else ("X", "O")
    return os.getenv("SYMBOLS").split(",") if os.getenv("SYMBOLS", None) else symbols

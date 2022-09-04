from ticTacToe.errors import InputException
from typing import Any
import os
from dotenv import load_dotenv

load_dotenv()


def get_input(input_text: str, validation_func, game_handler=None) -> Any:
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


# todo: fix symbols env
def get_symbols_env(symbols=None):
    symbols = symbols if symbols else ("X", "O")
    print(os.environ)
    return os.getenv("SYMBOLS", symbols)

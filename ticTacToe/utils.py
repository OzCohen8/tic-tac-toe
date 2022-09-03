from ticTacToe.errors import InputException
from typing import Any


def get_input(input_text: str, validation_func) -> Any:
    while True:
        try:
            input_args = input(input_text)
            if input_args.strip() == "showScores":
                pass
            validation_func(input_args)
            return input_args
        except InputException as e:
            print("Input exception; " + str(e))

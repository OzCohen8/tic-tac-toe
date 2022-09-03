from ticTacToe.errors import InputException
from typing import Any


def get_input(input_text: str, validation_func) -> Any:
    while True:
        input_args = input(input_text)
        try:
            validation_func(input_args)
            return input_args
        except InputException as e:
            if input_args.strip() == "showScores":
                pass
            print("Input exception; " + str(e))

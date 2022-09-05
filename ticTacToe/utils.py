from typing import Any, Dict
from dotenv import dotenv_values
from ticTacToe.errors import InputException

"""
common use function across the tic-tac-toe module
"""

config_parameters: Dict[str, Any] = dotenv_values(".env")
config_parameters = {"SYMBOL_A": "X", "SYMBOL_B": "O", "WIN_POINTS": 2, "TIE_POINTS": 1, "BOARD_RAW_SIZE": 3}
print(config_parameters)


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

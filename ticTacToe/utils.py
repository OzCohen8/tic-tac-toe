import json
from typing import Any, Dict, Tuple
from ticTacToe.errors import InputException

"""
common use function across the tic-tac-toe module
"""
with open("game_config.json", "r") as fp:
    config_parameters: Dict[str, Any] = json.load(fp)


def get_input(input_text: str, validation_func, game_handler=None) -> Any:
    """
    generic function to get input from the player, validate it, in case the input is not valid asks for the input again
    Args:
        input_text: the text that will be presented to the user while asking for the input
        validation_func: the validation which need to check against that input
        game_handler: (optional) the game state handler for the ability to show score any time the program ask for input
    Returns:
        the input params
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


def convert_spot_row_column(spot: int) -> Tuple[int, int]:
    """
    convert the spot(int from 1-9) to row and column on the board
    Args:
        spot: the spot we want to convert to row and column
    """
    row: int = (spot-1) // 3
    column: int = (spot-1) % 3
    return row, column



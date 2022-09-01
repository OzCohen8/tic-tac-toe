from typing import List
from gameBoard.game_handler import GameHandler


def run_game():
    print("Welcome to Oz's tic-tac-toe game!\nplease enter the players names, (can be one player or two :) )")
    # getting the players names
    while True:
        players: List[str] = input("Enter players names: ").split(',')
        if 0 < len(players) < 3:
            player1 = players[0].strip()
            player2 = players[1].strip()
            break
        print('only a single or two players can play')

    game_handler: GameHandler = GameHandler(player1=player1, player2=player2)
    game_handler.start_games()


if __name__ == '__main__':
    run_game()


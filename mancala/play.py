from mancala.board import Board
from mancala.utils.functions import print_board
import time
import random


def end_game_summary(board: Board, human_team_number, ai_team_number):
    print("Game is finished")
    stones_in_thrones = board.stones_in_thrones()
    human_score = stones_in_thrones[human_team_number]
    ai_score = stones_in_thrones[ai_team_number]
    print("Score: {} vs {}".format(human_score, ai_score))
    if human_score > ai_score:
        print(" Human wins")
    else:
        print(" AI wins")


def play_round(board: Board, human_team_number: int, ai_team_number: int):

    play_again = True

    while play_again:
        legal_moves = board.get_legal_moves(human_team_number)
        while True:
            action = int(input("Select Action"))
            if action not in legal_moves:
                print("Illegal move, please pick a dimple on your side of the board")
            else:
                break
        play_again = board.evacuate_dimple(action)
        print_board(board)

    if board.game_is_finished():
        end_game_summary(board, human_team_number, ai_team_number)
        return board, True

    play_again = True
    while play_again:
        time.sleep(1)
        legal_moves = board.get_legal_moves(ai_team_number)
        move = random.choice(legal_moves)
        board.evacuate_dimple(move)
        play_again = print_board(board)

    if board.game_is_finished():
        end_game_summary(board, human_team_number, ai_team_number)
        return board, True

    return board, False


def play_game(human_team_number=0):

    ai_team_number = 1 - human_team_number

    board = Board()
    print(f"YOU'RE TEAM NUMBER {human_team_number}")
    print_board(board)
    done = False
    while not done:
        board, done = play_round(board, human_team_number, ai_team_number)

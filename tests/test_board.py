"""
See picture of the board to understand the indicies
"""
from monazco.board import Board
import monazco.constants as cs
import pytest


@pytest.fixture
def board():
    the_board = Board()
    yield the_board
    del the_board


def test_generate_board(board: Board):

    assert len(board) == 14
    non_thrones = [i for i in range(14) if i not in [3, 10]]

    assert all([board[i].stones == cs.DEFAULT_STONES for i in non_thrones])
    assert board[3].stones == board[10].stones == 0

    assert board[3].is_throne == board[10].is_throne == True  # noqa
    assert all([not board[i].is_throne for i in non_thrones])

    team_1_count, team_2_count = 0, 0
    for dimple in board:
        if dimple.team == 0:
            team_1_count += 1
        if dimple.team == 1:
            team_2_count += 1
    assert team_1_count == team_2_count == 7


def test_legal_moves(board: Board):

    board[0].stones = 0
    assert 0 not in board.get_legal_moves(team_number=0)
    assert 1 not in board.get_legal_moves(team_number=1)


def test_stones_in_thrones(board: Board):

    assert board.stones_in_thrones() == (0, 0)
    board[cs.THRONE_1_NUM].stones = 10
    board[cs.THRONE_2_NUM].stones = 11
    assert board.stones_in_thrones() == (10, 11)


def test_stone_values(board: Board):

    assert board.stone_values() == cs.BASE_STONE_VALUES


def test_game_is_finished(board: Board):

    assert not board.game_is_finished()
    for i in [0, 1, 2, 3, 4, 5, 6]:
        board[i].stones = 0
    assert board.game_is_finished()
    board[0].stones = 1
    assert not board.game_is_finished()

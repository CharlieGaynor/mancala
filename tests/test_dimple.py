"""
See picture of the board to understand the indicies
"""
from mancala.board import Board
from mancala.nodes import Dimple
from mancala.utils.errors import EmptyDimpleError
from typing import Tuple
import mancala.constants as cs
import pytest


@pytest.fixture
def board():
    the_board = Board()
    yield the_board
    del the_board


def test_evacuate_standard(board: Tuple[Dimple]):
    play_again = board[0].evacuate()

    assert play_again == 1
    assert board[0].stones == 0
    assert board[1].stones == cs.DEFAULT_STONES + 1
    assert board[2].stones == cs.DEFAULT_STONES + 1
    assert board[3].stones == 1

    play_again = board[8].evacuate()
    assert play_again == 0
    assert board[8].stones == 0
    assert board[9].stones == cs.DEFAULT_STONES + 1
    assert board[10].stones == 1
    assert board[11].stones == cs.DEFAULT_STONES + 1


def test_finish_on_opposite(board: Tuple[Dimple]):
    board[1].stones = 0
    board[0].stones = 1
    board[5].stones = 10

    play_again = board[0].evacuate()

    assert play_again == 0
    assert board[0].stones == 0
    assert board[1].stones == 0
    assert board[5].stones == 0
    assert board[3].stones == 11

    board[8].stones = 0
    board[7].stones = 1
    board[12].stones = 10

    play_again = board[7].evacuate()

    assert play_again == 0
    assert board[7].stones == 0
    assert board[8].stones == 0
    assert board[12].stones == 0
    assert board[10].stones == 11


def test_skip_throne(board: Tuple[Dimple]):
    board[5].stones = 100

    board[5].evacuate()

    assert board[10].stones == 0


def test_evacuate_empty(board: Tuple[Dimple]):
    board[0].stones = 0
    with pytest.raises(EmptyDimpleError):
        board[0].evacuate()

"""
See picture of the board to understand the indicies
"""
from monazco.board import Board
from monazco.gymlike_env import MonazcoEnv
import pytest
import monazco.constants as cs


@pytest.fixture
def board():
    the_board = Board()
    yield the_board
    del the_board


@pytest.fixture
def env():
    monazco = MonazcoEnv()
    yield monazco
    del monazco


def test_reset(env: MonazcoEnv):
    (obs, legal_moves), info = env.reset()

    assert env._ai_team in [0, 1]
    assert env._player_team in [0, 1] and env._player_team != env._ai_team

    if env._player_team == 0:
        assert legal_moves == cs.PLAYER_1_MOVES
        assert obs == cs.BASE_STONE_VALUES
    else:
        assert legal_moves == cs.PLAYER_2_MOVES
        assert 0 in obs

    assert info.get("legal_moves") == True


def test_step(env: MonazcoEnv):
    (obs, legal_moves), info = env.reset(force_player_first=True)

    action = legal_moves[0]
    (obs, legal_moves), reward, done, terminated, info = env.step(action)

    assert obs[action] == 0
    assert reward == env._board[cs.THRONE_1_NUM].stones
    assert not done
    assert action not in legal_moves

    (obs, legal_moves), info = env.reset(force_player_first=True)

    action = 0
    (obs, legal_moves), reward, done, terminated, info = env.step(action)

    assert all([env._board[i].stones == cs.DEFAULT_STONES for i in cs.PLAYER_2_MOVES])
    assert env._board[cs.THRONE_2_NUM].stones == 0

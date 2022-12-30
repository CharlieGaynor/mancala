from typing import Tuple, List
from mancala.board import Board
import mancala.constants as cs
import mancala.utils.errors as er
import random


class MancalaEnv:
    def __init__(self) -> None:
        self._player_team: int = 0
        self._ai_team: int = 0
        self._board: Board = Board()

    def step(self, dimple_num: int) -> Tuple[List, float, bool, bool, None]:
        """
        Args:
            card (int): Which card to play - [0, 51]

        Returns:
            (obs, legal_moves, reward, done, terminated, info)
        """
        if dimple_num in cs.THRONE_NUMS:
            raise er.BadDimpleNumber("You've tried to evacuate a throne! can't be done sunny Jim")
        _dimple = self._board[dimple_num]
        if self._player_team != _dimple.team:
            raise er.WrongTeamErorr("You've selected a dimple which does not belong to you")
        playing_again = self._board.evacuate_dimple(dimple_num)
        done = self._board.game_is_finished()
        if not playing_again:
            self._play_ai_turns()

        obs = self._board.stone_values()
        _throne_values = self._board.stones_in_thrones()
        # Other possible rewards:
        # Difference in throne values, whether we have more stones in throne, whether we have won or not
        reward = _throne_values[self._player_team]

        return (obs, self._board.get_legal_moves(self._player_team)), reward, done, done, {'legal_moves': True}

    def reset(self, force_player_first=False) -> Tuple[List, None]:
        """Prepare environment for next round"""
        self._board.generate_board()

        if force_player_first:
            self._player_team = 0
            self._ai_team = 1
        else:
            self._ai_team = random.randint(0, 1)
            self._player_team = 1 - self._ai_team

        if self._ai_team == 0:
            self._play_ai_turns()
        obs = self._board.stone_values()
        legal_moves = self._board.get_legal_moves(self._player_team)
        return (obs, legal_moves), {'legal_moves': True}

    def _play_ai_turns(self) -> None:
        play_again = True
        while play_again and not self._board.game_is_finished():
            legal_moves = self._board.get_legal_moves(self._ai_team)
            move = random.choice(legal_moves)
            play_again = self._board.evacuate_dimple(move)

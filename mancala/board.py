from mancala.nodes import Dimple
from typing import Tuple, List
import mancala.constants as cs


class Board:
    def __init__(self) -> None:
        self.generate_board()

    def __getitem__(self, index):
        return self.board[index]

    def __setitem__(self, index, value):
        self.board[index] = value

    def __len__(self):
        return len(self.board)

    def game_is_finished(self) -> bool:
        if (
            sum([self[i].stones for i in cs.PLAYER_1_MOVES]) == 0
            or sum([self[i].stones for i in cs.PLAYER_2_MOVES]) == 0
        ):
            return True
        return False

    def stone_values(self) -> List[int]:
        return [self[i].stones for i in range(len(self))]

    def stones_in_thrones(self) -> Tuple[int]:
        return (self[3].stones, self[10].stones)

    def evacuate_dimple(self, index) -> bool:
        return self[index].evacuate()

    def get_legal_moves(self, team_number) -> List[int]:
        if team_number == 0:
            nodes = cs.PLAYER_1_MOVES
        else:
            nodes = cs.PLAYER_2_MOVES

        return [i for i in nodes if self[i].stones != 0]

    def generate_board(self) -> Tuple[Dimple]:
        throne_1 = Dimple(team=0, throne=None, is_throne=True, stones=0)
        throne_2 = Dimple(team=1, throne=None, is_throne=True, stones=0)
        dimples_1 = [Dimple(team=0, throne=throne_1, is_throne=False, stones=cs.DEFAULT_STONES) for _ in range(6)]
        dimples_2 = [Dimple(team=1, throne=throne_2, is_throne=False, stones=cs.DEFAULT_STONES) for _ in range(6)]

        # Assigning the cyclical pattern
        dimple_order = (
            dimples_1[0],
            dimples_1[1],
            dimples_1[2],
            throne_1,
            dimples_1[3],
            dimples_1[4],
            dimples_1[5],
            dimples_2[0],
            dimples_2[1],
            dimples_2[2],
            throne_2,
            dimples_2[3],
            dimples_2[4],
            dimples_2[5],
        )

        for dimp1, dimp2 in zip(dimple_order[:-1], dimple_order[1:]):
            dimp1.next = dimp2
        dimple_order[-1].next = dimple_order[0]

        # Assinging opposites
        def assign_opposites(dimple1: Dimple, dimple2: Dimple):
            dimple1.opposite = dimple2
            dimple2.opposite = dimple1

        pairs = ((0, 5), (1, 4), (2, 3))
        for idx1, idx2 in pairs:
            assign_opposites(dimples_1[idx1], dimples_1[idx2])
            assign_opposites(dimples_2[idx1], dimples_2[idx2])

        self.board = dimple_order

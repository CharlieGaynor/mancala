from monazco.utils import errors
from typing import TypeVar

DIMP = TypeVar("DIMP", bound="Dimple")


class Dimple:
    def __init__(self, team: int, throne: DIMP, opposite: DIMP = None, is_throne: bool = False, stones: int = 3):
        self.next: DIMP = None

        self.team = team
        self.throne = throne  # Reference to the throne of the same team
        self.opposite = opposite  # Reference to the dimple opposite
        self.is_throne = is_throne

        self.stones = stones

    def transfer_stones(self, other_dimple: DIMP) -> None:
        other_dimple.stones += self.stones
        self.stones = 0

    def evacuate(self) -> bool:
        """Move the stones counter clockwise one at a time. Return True if the same player should play again"""
        if self.stones == 0:
            raise errors.EmptyDimpleError("No stones in this dimple!")

        next_dimple = self
        for _ in range(self.stones):
            next_dimple = next_dimple.next
            if next_dimple.is_throne and next_dimple.team != self.team:
                next_dimple = next_dimple.next
            next_dimple.stones += 1

        # Empty dimple
        self.stones = 0

        final_dimple = next_dimple

        # If we finished on a (was) empty dimple (in our team), empty this dimple and the one opposite.
        if final_dimple.stones == 1 and final_dimple.team == self.team and not final_dimple.is_throne:
            final_dimple.transfer_stones(self.throne)
            final_dimple.opposite.transfer_stones(self.throne)

        # If we fininished on the throne then return 1 (meaning we go again)
        if final_dimple.is_throne:
            return True
        else:
            return False

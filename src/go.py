"""
Module providing a Go class
"""
from base import GoBase

#Description available in base.py
BoardGridType = list[list[int | None]]
ListMovesType = list[tuple[int, int]]


class Go(GoBase):
    """
    Class representing the game Go
    """

    _side: int
    _players: int
    _superko: bool

    def __init__(self, side: int, players: int, superko: bool = False):
        self._side = side
        self._players = players
        self._superko = superko

    def grid(self) -> BoardGridType:
        raise NotImplementedError

    @property
    def turn(self) -> int:
        raise NotImplementedError

    @property
    def available_moves(self) -> ListMovesType:
        raise NotImplementedError

    @property
    def done(self) -> bool:
        raise NotImplementedError

    @property
    def outcome(self) -> list[int]:
        raise NotImplementedError

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        raise NotImplementedError

    def legal_move(self, pos: tuple[int, int]) -> bool:
        raise NotImplementedError

    def apply_move(self, pos: tuple[int, int]) -> None:
        raise NotImplementedError

    def pass_turn(self) -> None:
        raise NotImplementedError

    def scores(self) -> dict[int, int]:
        raise NotImplementedError

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        raise NotImplementedError

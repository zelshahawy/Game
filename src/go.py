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
    #was there any point to add the innit if it inherits from go base. also the specification of properties
    #docstrings

    def __init__(self, side: int, players: int, superko: bool = False):
        super().__init__(side, players, superko)

    def grid(self) -> BoardGridType:
        """
        See GoBase.grid
        """
        raise NotImplementedError

    @property
    def turn(self) -> int:
        """
        See GoBase.turn
        """
        raise NotImplementedError

    @property
    def available_moves(self) -> ListMovesType:
        """
        See GoBase.available_moves
        """
        raise NotImplementedError

    @property
    def done(self) -> bool:
        """
        See GoBase.done
        """
        raise NotImplementedError

    @property
    def outcome(self) -> list[int]:
        """
        See GoBase.outcome
        """
        raise NotImplementedError

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        """
        See GoBase.piece_at
        """
        raise NotImplementedError

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        See GoBase.legal_move
        """
        raise NotImplementedError

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        See GoBase.apply_move
        """
        raise NotImplementedError

    def pass_turn(self) -> None:
        """
        See GoBase.pass_turn
        """
        raise NotImplementedError

    def scores(self) -> dict[int, int]:
        """
        See GoBase.scores
        """
        raise NotImplementedError

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        See GoBase.load_game
        """
        raise NotImplementedError

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        """
        See GoBase.simulate_move
        """
        raise NotImplementedError

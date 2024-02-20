"""
Module providing the Go class
"""
from copy import deepcopy

from base import GoBase
from board import Board

BoardGridType = list[list[int | None]]
ListMovesType = list[tuple[int, int]]

class Go(GoBase):
    """
    Class representing the game Go
    """
    def __init__(self, side: int, players: int, superko: bool = False):
        """
        See GoBase.__init__
        """
        super().__init__(side, players, superko)
        if side < 2:
            raise ValueError("Board size must be at least 2x2")
        
        self._board = Board(side, side)
        self._turn = 1
        self._num_moves = 0
        self._consecutive_passes = 0

        if self._superko:
            self._previous_boards: list[Board] = {}
        else:
            self._previous_board: Board | None = None

    @property
    def size(self) -> int:
        """
        See GoBase.size
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        See GoBase.num_players
        """
        return self._players

    @property
    def grid(self) -> BoardGridType:
        """
        See GoBase.grid
        """
        return deepcopy(self._board._grid)

    @property
    def turn(self) -> int:
        """
        See GoBase.turn
        """
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        """
        See GoBase.available_moves
        """
        moves = []
        for row in range(self._side):
            for col in range(self._side):
                if self._board.get(row, col) is None:
                    moves.append((row, col))
        return moves

    @property
    def done(self) -> bool:
        """
        See GoBase.done
        """
        return self._consecutive_passes == self._players

    @property
    def outcome(self) -> list[int]:
        """
        See GoBase.outcome
        """
        if not self.done:
            return []
        scores = self.scores()
        max_score = max(scores.values())
        winners = []
        for player, score in scores.items():
            if score == max_score:
                winners.append(player)
        return winners

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

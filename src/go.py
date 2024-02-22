"""
Module providing the Go class
"""
from copy import deepcopy
from typing import Optional

from base import GoBase, BoardGridType, ListMovesType
from board import Board


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
        self._consecutive_passes = 0

        if self._superko:
            self._previous_boards: list[BoardGridType] = []
        else:
            self._previous_board: BoardGridType | None = None

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
        return deepcopy(self._board.grid)

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
        if not self._board.valid_position(*pos):
            raise ValueError("Position is outside the bounds of the board.")
        return self._board.get(*pos)

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        See GoBase.legal_move
        """
        if not self._board.valid_position(*pos):
            raise ValueError("Position is outside the bounds of the board.")

        resulting_board = self.simulate_move(pos).grid
        if self._superko and resulting_board in self._previous_boards:
            return False
        elif not self._superko and resulting_board == self._previous_board:
            return False
        if self._board.get(*pos) is not None:
            return False
        return True

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        See GoBase.apply_move
        """
        if not self._board.valid_position(*pos):
            raise ValueError("Position is outside the bounds of the board.")
        if self._superko:
            self._previous_boards.append(self.grid)
        else:
            self._previous_board = self.grid
        self._board.set(*pos, self._turn)


        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            adjacent_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if self._board.valid_position(*adjacent_pos):
                if self.piece_at(adjacent_pos) not in {None, self._turn}:
                    if not self.has_liberties(adjacent_pos):
                        self.remove_group(adjacent_pos)
        self.pass_turn()
        self._consecutive_passes = 0

    def has_liberties(self, pos :tuple [int, int]) -> bool:
        """
        Calculates the liberties of each stone on the keyboard
        """

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            adjacent_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if self._board.valid_position(*adjacent_pos) and self.piece_at(adjacent_pos) is None:
                return True
        return False

    def remove_group(self, pos: tuple[int, int]) -> None:
        """
        Remove a group of stones from the board.
        """
        color = self._board.get(*pos)
        if color is None:
            return

        group = set()
        stack = [pos]
        while stack:
            current_pos = stack.pop()
            group.add(current_pos)

            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                adjacent_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if self._board.valid_position(*adjacent_pos) and self._board.get(*adjacent_pos) == color and adjacent_pos not in group:
                    stack.append(adjacent_pos)

        for pos in group:
            self._board.set(*pos, None)

    def adjacent_stones(self, pos : tuple[int, int]) -> list[Optional[int]]:
        """
        Creates a list of adjacent stones near a stone at specific pos
        """
        adj_stones: list[Optional[int]] = []

        for pos in self._board.adjacent_positions(pos):
            adj_stones.append(self.piece_at(pos))

        return adj_stones

    def capture_stones(self) -> None:
        """
        Removes a stone in the board if it lacks territories
        """
        for i in range(self.size):
            for j in range(self.size):
                if not self.has_liberties((i,j)):
                    self._board.set(i ,j, None)  

    def pass_turn(self) -> None:
        """
        See GoBase.pass_turn
        """
        self._consecutive_passes += 1
        self._turn = (self._turn % self._players) + 1

    def scores(self) -> dict[int, int]:
        """
        See GoBase.scores
        """
        scores = {player: 0 for player in range(1, self._players + 1)}
        for row in range(self._side):
            for col in range(self._side):
                piece = self.piece_at((row, col))
                if piece is not None:
                    scores[piece] += 1
        return scores

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        See GoBase.load_game
        """
        if turn > self._players:
            raise ValueError("Invalid turn number")
        if len(grid) != self._side:
            raise ValueError("Invalid grid size")
        for row in range(len(grid)):
            for col in range(len(grid)):
                if grid[row][col] not in range(1, self._players+1):
                    raise ValueError(f"Invalid value in grid: {grid[row][col]}")

        self._previous_boards = []
        self._previous_board = None
        self._consecutive_passes = 0
        self._turn = turn
        self._board._grid = grid


    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        """
        See GoBase.simulate_move
        """
        if pos is not None and not self._board.valid_position(*pos):
            raise ValueError("Position is outside the bounds of the board.")
        new_game = deepcopy(self)
        if pos is not None:
            new_game.apply_move(pos)
        else:
            new_game.pass_turn()
        return new_game

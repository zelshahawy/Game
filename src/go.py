"""
Module providing the Go class
"""
from copy import deepcopy
from typing import Optional

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
        if resulting_board == self._previous_board:
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
            self._previous_boards.append((self.grid))
        else:
            self._previous_board = self.grid

        self._board.set(*pos, self._turn)

        self.capture_stones()

        self.pass_turn()
        self._consecutive_passes = 0

    def has_liberties(self, pos :tuple [int, int]) -> bool:
        """
        Calculates the liberties of each stone on the keyboard
        """
        count :int = 0

        for stone in self.adjacent_stones(pos):
            if stone == self.piece_at(pos) or stone is None:
                count += 1

        return count > 0

    def adjacent_stones(self, pos : tuple[int, int]) -> list[Optional[int]]:
        """
        Creates a list of adjacent stones near a stone at specific pos
        """
        adj_stones :list[Optional[int]] = []
    
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
        for row in grid:
            for col in grid:
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

if __name__ == "__main__":
    go = Go(6,2,False)
    go.apply_move((3,2)) #white
    go.apply_move((2,1)) #black
    go.pass_turn()
    go.apply_move((3,3)) #black
    go.pass_turn() #white
    go.apply_move((3,1)) #black
    go.pass_turn()
    go.apply_move((4,2)) #black
    go.pass_turn()
    go.apply_move((3,0)) #black
    go.pass_turn()
    go.apply_move((2,2)) #black


    print(f"Stones at {go.piece_at((3,2))} ")
    print(f"adjacent stones {go._board.adjacent_positions((3,2))} at 3, 2 is {go.adjacent_stones((3,2))}")
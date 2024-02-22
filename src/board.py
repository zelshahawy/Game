"""
A class to represent a board.
"""
from copy import deepcopy
from typing import Optional
from base import BoardGridType

class Board:
    """
    A class to represent a board.
    """
    _rows: int
    _cols: int
    _grid: BoardGridType

    def __init__(self, rows: int, cols: int) -> None:
        self._rows = rows
        self._cols = cols
        self._grid = [[None for _ in range(cols)] for _ in range(rows)]

    @property
    def rows(self) -> int:
        """
        Get the number of rows in the board.
        """
        return self._rows

    @property
    def cols(self) -> int:
        """
        Get the number of columns in the board.
        """
        return self._cols

    @property
    def grid(self) -> BoardGridType:
        """
        get a copy of the grid of the board.
        """
        return deepcopy(self._grid)

    def set(self, row: int, col: int, value: int | None) -> None:
        """
        Set the value of the board at a given position.
        """
        self._grid[row][col] = value

    def get(self, row: int, col: int) -> Optional[int]:
        """
        Get the value of the board at a given position.
        """
        return self._grid[row][col]

    def valid_position(self, row: int, col: int) -> bool:
        """
        Check if the position is valid.
        """
        return 0 <= row < self._rows and 0 <= col < self._cols

    def adjacent_positions(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Returns a list of all valid positions adjacent to the specified
        position.
        """
        positions = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            potential_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if self.valid_position(*potential_pos):
                positions.append(potential_pos)
        return positions

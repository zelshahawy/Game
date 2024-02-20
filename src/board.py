"""
A class to represent a board.
"""
from typing import Optional

class Board:
    """
    A class to represent a board.
    """
    _rows: int
    _cols: int
    _grid: list[list[Optional[int]]]

    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = [[None for _ in range(cols)] for _ in range(rows)]

    @property
    def rows(self):
        """
        Get the number of rows in the board.
        """
        return self._rows

    @property
    def cols(self):
        """
        Get the number of columns in the board.
        """
        return self._cols

    def set(self, row, col, value):
        """
        Set the value of the board at a given position.
        """
        self._grid[row][col] = value

    def get(self, row, col):
        """
        Get the value of the board at a given position.
        """
        return self._grid[row][col]

    def valid_position(self, row, col):
        """
        Check if the position is valid.
        """
        return 0 <= row < self._rows and 0 <= col < self._cols

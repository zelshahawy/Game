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
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            raise ValueError("Position out of bounds")
        return self._grid[row][col]

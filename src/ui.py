"""
Abstract class for graphical and text user interface
"""
from abc import ABC, abstractmethod
from fakes import GoFake

class GoUI(ABC):
    """
    Abstract class for Go graphical and text user interface
    """
    _go: GoFake

    def __init__(self, go: GoFake) -> None:
        """
        Constructor

        Args:
            go_game: The Go game to display and interact with
        """
        self._go = go

    @abstractmethod
    def display_board(self) -> None:
        """
        Displays current Go board
        """
        raise NotImplementedError

    @abstractmethod
    def get_move(self) -> tuple[int, int]:
        """
        Retrieves and returns the current player's move
        """
        raise NotImplementedError

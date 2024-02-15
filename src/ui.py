"""
Abstract class for graphical and text user interface
"""
from abc import ABC, abstractmethod
from fakes import GoStub

class GoUI(ABC):
    """
    Abstract class for Go graphical and text user interface
    """
    _go_game: GoStub

    def __init__(self, go_game: GoStub) -> None:
        """
        Constructor

        Args:
            go_game: The Go game to display and interact with
        """
        self._go_game = go_game

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

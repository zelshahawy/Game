"""
Base class for the bot implementation
"""

from abc import ABC, abstractmethod
from enum import IntEnum
from fakes import GoStub



class Players(IntEnum):
    """Enumeration for Player 1 and Player 2."""
    BLACK = 1
    WHITE = 2


class BaseBot(ABC):
    """
    Base class for a bot in a Go Game
    """

    @abstractmethod
    def make_move(self, game: GoStub) -> None:
        """
        perform a move in a game of go
        """
        raise NotImplementedError

    @abstractmethod
    def show_player(self) -> Players:
        """
        reveals the color of a players
        """
        raise NotImplementedError


class SimulateBots(ABC):
    """
    Simulate a bot 
    """

    @abstractmethod
    def simulate_games(self, num_of_games: int) -> tuple[float, float, float]:
        """
        sunulate a game between a list of robots
        """
        raise NotImplementedError

    @abstractmethod
    def update_results(self, results: list[int]) -> None:
        """
        Update the win/tie counts based on the outcome of a game.

        results: The outcome of a game.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_percentages(self, num_of_games: int) -> tuple[float, float, float]:
        """
        Calculate the win/tie percentages.

        num_of_games: The number of games simulated.
        return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        raise NotImplementedError

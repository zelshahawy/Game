from abc import ABC, abstractmethod


class BaseBot(ABC):
    """
    Base class for a bot in a Go Game
    """

    @abstractmethod
    def make_move(self) -> None:
        """
        perform a move in a game of go
        """
        raise NotImplementedError

class SimulateBots(ABC):
    """
    Simulate a bot 
    """

    @abstractmethod
    def simulate_games(self, num_of_games: int) -> tuple[float, float, float]:
        """
        """
        raise NotImplementedError

    @abstractmethod
    def update_results(self, results) -> None:
        raise NotImplementedError

    @abstractmethod
    def calculate_percentages(self, num_of_games) ->tuple[float, float, float]:
        raise NotADirectoryError
    
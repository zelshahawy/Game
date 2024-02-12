from abc import ABC, abstractmethod


class BaseBot(ABC):
    """
    """

    @abstractmethod
    def make_move(self):
        """
        """
        raise NotImplementedError

class SimulateBots(ABC):
    """
    """

    @abstractmethod
    def simulate_games(self, num_of_games:int, bots_used: set[BaseBot]):
        """
        """
        raise NotImplementedError
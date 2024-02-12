import sys
import random
from enum import IntEnum
from fakes import GoStub
from botbase import BaseBot, SimulateBots


class Players(IntEnum):
    """Enumeration for Player 1 and Player 2."""
    PLAYER1 = 0
    PLAYER2 = 1


class RandomBot(BaseBot):
    """Bot that makes random legal moves in a Go game."""

    game: GoStub
    def __init__(self, game: GoStub):
        """
        Initialize the bot with the game.

        game: The game the bot will be playing.
        """
        self._game = game

    def make_move(self) -> None:
        """
        Make a random legal move in the game.
        """
        move = random.choice(self._game.available_moves)
        while not self._game.legal_move(move):
            move = random.choice(self._game.available_moves)
        self._game.apply_move(move)


class RandomSimulation(SimulateBots):
    """Simulates a number of games between two RandomBots."""

    game: GoStub
    def __init__(self, game: GoStub) -> None:
        """
        Initialize the simulation with the game.

        game: The game the bots will be playing.
        """
        self._game = game
        self._bot1 = self._bot2 = RandomBot(self._game)
        self._bot1_wins = self._bot2_wins = self._ties = 0

    def simulate_games(self, num_of_games: int) -> tuple[float, float, float]:
        """
        Simulate a number of games and return the win percentages.

        :param num_of_games: The number of games to simulate.
        :return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        for _ in range(num_of_games):
            while not self._game.done:
                if self._game.turn == Players.PLAYER1:
                    self._bot1.make_move()
                else:
                    self._bot2.make_move()

            self.update_results(self._game.outcome)
            self._game = GoStub(self._game.size, self._game.num_players)
            self._bot1 = RandomBot(self._game)
            self._bot2 = RandomBot(self._game)
        return self.calculate_percentages(num_of_games)

    def update_results(self, results) -> None:
        """
        Update the win/tie counts based on the outcome of a game.

        results: The outcome of a game.
        """
        if len(results) == 2:
            self._ties += 1
        elif results[0] == 1:
            self._bot1_wins += 1
        elif results[0] == 2:
            self._bot2_wins += 1

    def calculate_percentages(self, num_of_games) ->tuple[float, float, float]:
        """
        Calculate the win/tie percentages.

        num_of_games: The number of games simulated.
        return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        wining_percentage_1 = (self._bot1_wins / num_of_games) * 100
        wining_percentage_2 = (self._bot2_wins / num_of_games) * 100
        tie_percentage = (self._ties) / (num_of_games) * 100
        return (wining_percentage_1, wining_percentage_2, tie_percentage)


def main(num_games):
    """
    Run the simulation and print the results.

    num_games: The number of games to simulate.
    """
    current_game = GoStub(9, 2)
    random_simulation = RandomSimulation(current_game)
    player1_win_percentage, player2_win_percentage, ties_percentage = \
        random_simulation.simulate_games(num_games)
    print(f"Player 1 wins: {player1_win_percentage:.2f}%")
    print(f"Player 2 wins: {player2_win_percentage:.2f}%")
    print(f"Ties: {ties_percentage:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error in the number of arguments. Usage: python3 src/bot.py NUM_GAMES")
        sys.exit(1)
    main(int(sys.argv[1]))

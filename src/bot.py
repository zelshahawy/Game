"""
Bot implementation for the Go game
"""

import sys
import random
from fakes import GoStub
from botbase import BaseBot, SimulateBots
from botbase import Players

class RandomBot(BaseBot):
    """Bot that makes random legal moves in a Go game."""

    game: GoStub

    def __init__(self, player):

        """
        Initialize the bot with the game.

        game: The game the bot will be playing.
        """
        self._player = player

    def show_player(self) -> Players:
        """
        return the color of the bot
        """
        return self._player

    def make_move(self, game) -> None:
        """
        Make a random legal move in the game.
        """
        move = random.choice(game.available_moves)
        while not game.legal_move(move):
            move = random.choice(game.available_moves)
        game.apply_move(move)


class Simulation(SimulateBots):
    """Simulates a number of games between two RandomBots."""

    game: GoStub
    bots: list[BaseBot]

    def __init__(self, game: GoStub, bots: list[BaseBot]) -> None:
        """
        Initialize the simulation with the game.

        game: The game the bots will be playing.
        """
        self._game = game
        self._bots = bots
        self._wins = {player: 0 for player in Players}
        self._ties = 0

    def reset_game(self):
        """
        resets a game to its default, beginning state
        """
        size = self._game.size
        num_of_players = self._game.num_players
        self._game = GoStub(size, num_of_players)

    def simulate_games(self, num_of_games: int) -> tuple[float, float, float]:
        """
        Simulate a number of games and return the win percentages.

        :param num_of_games: The number of games to simulate.
        :return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        for _ in range(num_of_games):
            while not self._game.done:
                for bot in self._bots:
                    if self._game.turn == bot.show_player():
                        bot.make_move(self._game)
            self.update_results(self._game.outcome)
            self.reset_game()
        return self.calculate_percentages(num_of_games)

    def update_results(self, results) -> None:
        """
        Update the win/tie counts based on the outcome of a game.

        results: The outcome of a game.
        """
        if len(results) == 2:
            self._ties += 1
        else:
            for bot in self._bots:
                if results[0] == bot.show_player():
                    self._wins[bot.show_player()] += 1

    def calculate_percentages(self, num_of_games) ->tuple[float, float, float]:
        """
        Calculate the win/tie percentages.

        num_of_games: The number of games simulated.
        return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        wining_percentage_1 = (self._wins[Players.BLACK] / num_of_games) * 100
        wining_percentage_2 = (self._wins[Players.WHITE] / num_of_games) * 100
        tie_percentage = (self._ties) / (num_of_games) * 100
        return (wining_percentage_1, wining_percentage_2, tie_percentage)


def random_main(num_games) -> None:
    """
    Run the simulation and print the results.

    num_games: The number of games to simulate.
    """
    current_game = GoStub(9, 2)
    bot1 = RandomBot(Players.BLACK)
    bot2 = RandomBot(Players.WHITE)
    random_simulation = Simulation(current_game, [bot1, bot2])
    player1_win_percentage, player2_win_percentage, ties_percentage = \
        random_simulation.simulate_games(num_games)
    print(f"Player 1 wins: {player1_win_percentage:.2f}%")
    print(f"Player 2 wins: {player2_win_percentage:.2f}%")
    print(f"Ties: {ties_percentage:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error in the number of arguments. Usage: python3 src/bot.py NUM_GAMES")
        sys.exit(1)
    random_main(int(sys.argv[1]))

"""
Bot implementation for the Go game
"""

import sys
import random
from fakes import GoFake
from botbase import BaseBot, SimulateBots
from botbase import Players

class RandomBot(BaseBot):
    """Bot that makes random legal moves in a Go game."""

    player: Players

    #init method inhereted

    #show player inhereted

    def make_move(self, game: GoFake) -> None:
        """
        Make a random legal move in the game.
        """
        if len(game.available_moves) == 1 and game.available_moves[0] == (0,0):
            game.pass_turn()
        move = random.choice(game.available_moves)
        while not game.legal_move(move):
            move = random.choice(game.available_moves)
        game.apply_move(move)

class SmartBot(BaseBot):
    """
    Bots that analyze not just the next move, but all the possible scenarios
    that will happen a few moves in the future, and choose the move that gets
    the player closer to winning.
    """
    #init method inhereted

    #show player inhereted

    def make_move(self, game: GoFake) -> None:
        best_move = None
        best_value = 0
        if len(game.available_moves) == 1 and game.available_moves[0] == (0,0):
            game.pass_turn()
        for move in game.available_moves:
            if move != (0, 0):
                simulated_game = game.simulate_move(move)
                opp_moves = simulated_game.available_moves
                total_pieces = 0
                for opp_move in opp_moves:
                    if opp_move != (0,0):
                        opp_simulation = simulated_game.simulate_move(opp_move)
                        total_pieces += opp_simulation.scores()[self.show_player()]
                average_pieces = total_pieces
                if average_pieces > best_value:
                    best_move = move
                    best_value = average_pieces
        game.apply_move(best_move)

class Simulation(SimulateBots):
    """Simulates a number of games between two RandomBots."""

    game: GoFake
    bots: list[BaseBot]

    def __init__(self, game: GoFake, bots: list[BaseBot]) -> None:
        """
        Initialize the simulation with the game.

        game: The game the bots will be playing.
        """
        self._game = game
        self._bots = bots
        self._wins = {player: 0 for player in Players}
        self._ties = 0
        self.total_moves = 0

    def reset_game(self) -> None:
        """
        resets a game to its default, beginning state
        """
        size = self._game.size
        num_of_players = self._game.num_players
        self._game = GoFake(size, num_of_players)

    def simulate_games(self, num_of_games: int) -> tuple[float, float, float]:
        """
        Simulate a number of games and return the win percentages.

        :param num_of_games: The number of games to simulate.
        :return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        for _ in range(num_of_games):
            while not self._game.done:
                if self._game._num_moves == 256:
                    break
                for bot in self._bots:
                    if self._game.turn == bot.show_player():
                        bot.make_move(self._game)
                        self.total_moves += 1
            self.update_results(self._game.outcome)
            self.reset_game()
        return self.calculate_percentages(num_of_games)

    def update_results(self, results: list[int]) -> None:
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

    def calculate_percentages(self, num_of_games: int) -> \
        tuple[float, float, float]:
        """
        Calculate the win/tie percentages.

        num_of_games: The number of games simulated.
        return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        wining_percentage_1 = (self._wins[Players.BLACK] / num_of_games) * 100
        wining_percentage_2 = (self._wins[Players.WHITE] / num_of_games) * 100
        tie_percentage = (self._ties) / (num_of_games) * 100
        average_moves_per_game = (self.total_moves) / (num_of_games)
        return (wining_percentage_1, wining_percentage_2, tie_percentage,
                average_moves_per_game)


def random_main(num_games: int) -> None:
    """
    Run the simulation and print the results.

    num_games: The number of games to simulate.
    """
    current_game = GoFake(6, 2)
    bot2 = SmartBot(Players.BLACK)
    bot1 = RandomBot(Players.WHITE)
    random_simulation = Simulation(current_game, [bot1, bot2])
    player_black_win_percentage, player_white_win_percentage, ties_percentage, average_moves_per_game = \
        random_simulation.simulate_games(num_games)
    print(f"Player 1 wins: {player_black_win_percentage:.2f}%")
    print(f"Player 2 wins: {player_white_win_percentage:.2f}%")
    print(f"Ties: {ties_percentage:.2f}%")
    print(f"Average moves: {average_moves_per_game:.1f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Error in the number of arguments." +
            " Usage: python3 src/bot.py NUM_GAMES"
        )
        sys.exit(1)
    random_main(int(sys.argv[1]))

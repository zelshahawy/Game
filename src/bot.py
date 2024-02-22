"""
Bot implementation for the Go game
"""

import sys
import random
from typing import Optional
from fakes import GoFake
from botbase import BaseBot, SimulateBots
from botbase import Players

class RandomBot(BaseBot):
    """Bot that makes random legal moves in a Go game."""

    player: Players

    #init method inherited

    #show player inherited

    def make_move(self, game: GoFake) -> None:
        """
        Make a random legal move in the game.
        """
        available_moves = [move for move in game.available_moves if move !=\
            (0,0) and game.legal_move(move)]
        if not available_moves:
            game.pass_turn()
            return
        move = random.choice(available_moves)
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
        possible_moves = [move for move in game.available_moves if game.legal_move(move)]
        if len(possible_moves) == 1 and possible_moves[0] == (0,0):
            game.pass_turn()
            return
        max_value: float | int = -1
        best_moves = []

        for move in possible_moves:
            if move == (0,0):
                game_copy = game.simulate_move(None)
            else:
                game_copy = game.simulate_move(move)
            next_moves = [move for move in game_copy.available_moves if game.legal_move(move)]
            total_pieces = 0
            for next_move in next_moves:
                if next_move == (0,0):
                    game_copy2 = game_copy.simulate_move(None)
                else:
                    game_copy2 = game_copy.simulate_move(next_move)
                    total_pieces += game_copy2.scores()[self.show_player()]

            value = total_pieces / len(next_moves) if next_moves else 0
            if value > max_value:
                max_value = value
                best_moves = [move]
            elif value == max_value:
                best_moves.append(move)
        if best_moves:
            best_move = random.choice(best_moves)
            if best_move == (0,0):
                game.pass_turn()
            else:
                game.apply_move(best_move)
        else:
            game.pass_turn()

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
        self._wins = {bot.show_player(): 0 for bot in bots}
        self._ties = 0
        self.total_moves = 0

    def reset_game(self) -> None:
        """
        resets a game to its default, beginning state
        """
        size = self._game.size
        num_of_players = self._game.num_players
        self._game = GoFake(size, num_of_players)

    def simulate_games(self, num_of_games: int) -> tuple[float, float, float, float]:
        """
        Simulate a number of games and return the win percentages.

        :param num_of_games: The number of games to simulate.
        :return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        for _ in range(num_of_games):
            while not self._game.done:
                if self._game.num_moves >= 256:
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
        if results:
            if len(results) == 2:
                self._ties += 1
            else:
                player = Players(results[0])
                self._wins[player] += 1
        else:
            scores = self._game.scores()
            max_score = max(scores.values())
            max_score_count = list(scores.values()).count(max_score)
            if max_score_count > 1:
                self._ties += 1
            else:
                max_score_player = max(scores, key=lambda player: scores[player])
                player = Players(max_score_player)
                self._wins[player] += 1
    def calculate_percentages(self, num_of_games: int) -> \
        tuple[float, float, float, float]:
        """
        Calculate the win/tie percentages.

        num_of_games: The number of games simulated.
        return: A tuple of the win percentages for bot1, bot2, and ties.
        """
        wining_percentage_black = (self._wins[Players.BLACK] / num_of_games) * 100
        wining_percentage_white = (self._wins[Players.WHITE] / num_of_games) * 100
        tie_percentage = (self._ties) / (num_of_games) * 100
        average_moves_per_game = (self.total_moves) / (num_of_games)
        return (wining_percentage_white, wining_percentage_black, tie_percentage,
                average_moves_per_game)


def main(num_games: int) -> None:
    """
    Run the simulation and print the results.

    num_games: The number of games to simulate.
    """
    current_game = GoFake(6, 2)
    bot_white = RandomBot(Players.WHITE)
    bot_black = SmartBot(Players.BLACK)
    random_simulation = Simulation(current_game, [bot_black, bot_white])
    player_white_win_percentage, player_black_win_percentage, ties_percentage, average_moves_per_game = \
        random_simulation.simulate_games(num_games)
    print(f"Player one (Random) wins: {player_white_win_percentage:.2f}%")
    print(f"Player two (Smart) wins: {player_black_win_percentage:.2f}%")
    print(f"Ties: {ties_percentage:.2f}%")
    print(f"Average moves: {average_moves_per_game:.1f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Error in the number of arguments." +
            " Usage: python3 src/bot.py NUM_GAMES"
        )
        sys.exit(1)
    main(int(sys.argv[1]))

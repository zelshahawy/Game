import sys
import random
from fakes import GoStub
from botbase import BaseBot, SimulateBots

class RandomBot(BaseBot):
    """
    """

    def __init__(self, game: GoStub):
        """
        """
        self.game = game
        
    def make_move(self):
        """
        """
        move = random.choice(self.game.available_moves)
        while not self.game.legal_move(move):
            move = random.choice(self.game.available_moves)
        self.game.apply_move(move)
        
class Simulation(SimulateBots):
    """
    """
    def __init__(self, game: GoStub, bots_used: list[BaseBot]) -> None:
        self.game = game
        self.bot1, self.bot2 = bots_used
        self.bot1_wins = self.bot2_wins = self.ties = 0


    def simulate_games(self, num_of_games: int):
        """
        """
        for _ in range(num_of_games):
            self.game = GoStub(self.game.size, self.game.num_players)
            while not self.game.done:
                if self.game.turn == 0:
                    self.bot1.make_move()
                else:
                    self.bot2.make_move()
                self.game.pass_turn()

            results = self.game.outcome
            if len(results) == 1:
                result = results[0]
                if result == 1:
                    self.bot1_wins += 1
                elif result == 2:
                    self.bot2_wins += 1
            else:
                self.ties += 1
        wining_percentage_1 = (self.bot1_wins / num_of_games) * 100
        wining_percentage_2 = (self.bot2_wins / num_of_games) * 100
        tie_percentage = (self.ties) / (num_of_games) * 100
        return (wining_percentage_1, wining_percentage_2, tie_percentage)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Error in the number of arguments. Usage: python3 src/bot.py NUM_GAMES")
        sys.exit(1)
    current_game = GoStub(9, 2)
    random_simulation = Simulation(current_game, [RandomBot(current_game), RandomBot(current_game)])
    num_games = int(sys.argv[1])
    player1_win_percentage, player2_win_percentage, ties_percentage = \
        random_simulation.simulate_games(num_games)
    print(f"Player 1 wins: {player1_win_percentage:.2f}%")
    print(f"Player 2 wins: {player2_win_percentage:.2f}%")
    print(f"Ties: {ties_percentage:.2f}%")

"""
TUI implementation for GoFake
"""
import sys
import time

from colorama import Fore, Style

from fakes import GoFake

PASS_MOVE = (-1, -1)

COLORS = [
    Fore.RED,
    Fore.BLUE,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
    Fore.BLACK
]

STONES = {
    i : COLORS[i] + "●" + Style.RESET_ALL for i in range(8)
}

class GoTUI():
    """
    Class for presenting TUI for a game of Go
    """
    go: GoFake

    def __init__(self, go: GoFake) -> None:
        """
        Constructor

        Args:
            go: The Go game to display and interact with
        """
        self._go = go

    def print_board(self) -> None:
        """
        Prints the current state of the board in the terminal

        Returns: nothing
        """
        size = self._go.size
        board = self._go.grid

        intersection_chars = {
            'first': ['┌', '├', '└'],
            'last': ['┐', '┤', '┘'],
            'middle': ['┬', '┼', '┴']
        }

        for i, row in enumerate(board):
            line = ""
            separator_line = ""
            for j, intersection in enumerate(row):
                intersection_type = 'first' if j == 0 else 'last' \
                    if j == size - 1 else 'middle'
                intersection_char = intersection_chars[intersection_type] \
                    [0 if i == 0 else 1 if i < size - 1 else 2]
                line += intersection_char if intersection is None \
                    else STONES[intersection]
                if j < size - 1:
                    line += "─"
                if j < size:
                    separator_line += "│ "
            print(line)
            if i < size - 1:
                print(separator_line)
    
    def print_scores(self) -> None:
        """
        Displays the scores of each player

        Returns: nothing
        """
        scores = self._go.scores()
        print(Fore.WHITE + "Scores:")
        for player, score in scores.items():
            print(f"{COLORS[player]} + Player {player}: {score} stones")

    def get_move(self) -> tuple[int, int]:
        """
        Retrieves and returns the current player's move

        Returns: the move
        """
        while True:
            time.sleep(0.2)
            move_input = input(
                Fore.GREEN +
                f"> It is player {self._go.turn}'s turn." +
                " Please enter a move [press Enter to pass]:\n"+
                Style.RESET_ALL
            )
            # Handle pass
            if move_input.strip() == "":
                return PASS_MOVE
            try:
                move = tuple(map(int, move_input.split()))
                if len (move) != 2 or move not in self._go.available_moves or \
                    not self._go.legal_move(move):
                    raise ValueError
                return move
            except ValueError:
                time.sleep(0.4)
                print(Fore.RED + "Invalid move. Please try again.")
                time.sleep(0.4)

    def end_game(self) -> None:
        """
        Prints game over message alongside the outcome of the game, then
        exits the game

        Returns: nothing
        """
        time.sleep(0.4)
        print(Fore.GREEN + "Game is over")
        for _ in range(3):
            print(".\n", end="", flush=True)
            time.sleep(0.4)
        if len(self._go.outcome) > 1:
            print(f"It's a tie!\n")
            self.print_scores()
        else:
            print(f"Player {self._go.outcome[0]} wins!\n")
            self.print_scores()
        sys.exit(0)

    def run_game(self) -> None:
        """
        Main event loop for the game, retrieves moves and displays board until
        the game is over

        Returns: nothing
        """
        self.print_board()
        while not self._go.done:
            move = self.get_move()
            if move == PASS_MOVE:
                self._go.pass_turn()
            else:
                self._go.apply_move(move)
            print("\033c", end="")
            self.print_board()
        self.end_game()


if __name__ == "__main__":
    try:
        side = sys.argv[1]
    except IndexError as exc:
        raise ValueError("Please provide the side length of the board") from exc
    
    tui = GoTUI(GoFake(int(side), 2))
    print("\033c", end="")
    # Welcome message
    _ = input(Fore.GREEN + ">>WELCOME TO 碁! PRESS ANY KEY TO START<<\n")
    print("\033c", end="")
    tui.run_game()

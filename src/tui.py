"""
TUI implementation for GoFake
"""
import sys
import time

from colorama import Fore, Style

from fakes import GoFake
from ui import GoUI

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

class GoTUI(GoUI):
    """
    Class for presenting TUI for a game of Go
    """
    def display_board(self) -> None:
        """
        See GoUI.display_board
        """
        size = self._go_game.size
        board = self._go_game.grid

        for i, row in enumerate(board):
            line = ""
            separator_line = ""
            for j, intersection in enumerate(row):
                first_intersection = "┌" if i == 0 else \
                      ("├" if i < size - 1 else "└")
                last_intersection = "┐" if i == 0 else \
                      ("┤" if i < size - 1 else "┘")
                middle_intersection = "┬" if i == 0 else \
                      ("┼" if i < size - 1 else "┴")

                # First intersection
                if j == 0:
                    line += first_intersection if intersection is None \
                        else STONES[intersection]
                # Last intersection
                elif j == size - 1:
                    line += last_intersection if intersection is None \
                        else STONES[intersection]
                # Middle intersections
                else:
                    line += middle_intersection if intersection is None \
                        else STONES[intersection]
                # Add horizontal separator for all intersections except last
                if j < size:
                    separator_line += "│ "
                if j < size - 1:
                    line += "─"
            print(line)
            if i < size - 1:
                print(separator_line)


    def get_move(self) -> tuple[int, int]:
        """
        See GoUI.get_move
        """
        while True:
            time.sleep(0.2)
            move_input = input(
                Fore.GREEN +
                f"> It is player {self._go_game.turn}'s turn." +
                " Please enter a move [press Enter to pass]:\n" +
                Style.RESET_ALL
            )
            # Handle pass
            if move_input.strip() == "":
                return None
            try:
                move = tuple(map(int, move_input.split()))
                if move not in self._go_game.available_moves or \
                    not self._go_game.legal_move(move):
                    raise ValueError
                return move
            except ValueError:
                time.sleep(0.4)
                print(Fore.RED + "Invalid move. Please try again." + \
                               Style.RESET_ALL)
                time.sleep(0.4)

    def display_game_over_msg(self) -> None:
        """
        Display game over message
        """
        time.sleep(0.4)
        print(Fore.GREEN + "Game is over")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.4)
        if len(self._go_game.outcome) > 1:
            print(f"It's a {Fore.CYAN}tie{Fore.GREEN}! " +
                  f"({self._go_game.scores()[1]} vs" +
                  f"{self._go_game.scores()[2]}){Style.RESET_ALL}")
        else:
            print(f"Player {self._go_game.outcome[0]} wins! " +
                   f"({self._go_game.scores()[1]} vs" +
                   f" {self._go_game.scores()[2]})")
        sys.exit(0)


def main() -> None:
    """
    Main TUI event loop
    """
    side = int(sys.argv[1])
    go = GoFake(side, 2)
    go_tui = GoTUI(go)

    print("\033c", end="")
    _ = input(Fore.GREEN + ">>WELCOME TO 碁! PRESS ANY KEY TO START<<\n"\
                    + Style.RESET_ALL)
    print("\033c", end="")

    go_tui.display_board()
    while True:
        if go.done:
            go_tui.display_game_over_msg()
        move = go_tui.get_move()
        if move is None:
            go.pass_turn()
        else:
            go.apply_move(move)
        print("\033c", end="")
        go_tui.display_board()

if __name__ == "__main__":
    main()

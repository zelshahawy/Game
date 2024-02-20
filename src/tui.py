"""
TUI implementation for GoFake
"""
from typing import Optional
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
        size = self._go.size
        board = self._go.grid

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
                f"> It is player {self._go.turn}'s turn." +
                " Please enter a move [press Enter to pass]:\n" +
                Style.RESET_ALL
            )
            # Handle pass
            if move_input.strip() == "":
                return (-1, -1)
            try:
                move = tuple(map(int, move_input.split()))
                if len (move) != 2 or move not in self._go.available_moves or \
                    not self._go.legal_move(move):
                    raise ValueError
                return move
            except ValueError:
                time.sleep(0.4)
                print(Fore.RED + "Invalid move. Please try again." + \
                               Style.RESET_ALL)
                time.sleep(0.4)

    def display_game_over_msg(self) -> None:
        """
        Displays game over message alongside the outcome of the game

        Returns: nothing
        """
        time.sleep(0.4)
        print(Fore.GREEN + "Game is over")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.4)
        if len(self._go.outcome) > 1:
            print(f"It's a {Fore.CYAN}tie{Fore.GREEN}! " +
                  f"({self._go.scores()[1]} vs" +
                  f"{self._go.scores()[2]}){Style.RESET_ALL}")
        else:
            print(f"Player {self._go.outcome[0]} wins! " +
                   f"({self._go.scores()[1]} vs" +
                   f" {self._go.scores()[2]})")

    def main_loop(self) -> None:
        """
        Main event loop for the game, retrieves moves and displays board

        Returns: nothing
        """
        print("\033c", end="")
        _ = input(Fore.GREEN + ">>WELCOME TO 碁! PRESS ANY KEY TO START<<\n"\
                        + Style.RESET_ALL)
        print("\033c", end="")

        self.display_board()
        while True:
            if self._go.done:
                self.display_game_over_msg()
                sys.exit(0)
            move = self.get_move()
            if move == (-1, -1):
                self._go.pass_turn()
            else:
                self._go.apply_move(move)
            print("\033c", end="")
            self.display_board()


if __name__ == "__main__":
    side = sys.argv[1]
    tui = GoTUI(GoFake(int(side), 2))
    tui.main_loop()

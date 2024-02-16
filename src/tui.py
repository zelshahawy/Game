"""
TUI implementation for GoStub
"""
import sys
import os
import time

from colorama import Fore, Style

from fakes import GoFake
from ui import GoUI

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
            for j, intersection in enumerate(row):
                first_intersection = (
                    "┌" if i == 0 else ("├" if i < size - 1 else "└")
                )
                last_intersection = (
                    "┐" if i == 0 else ("┤" if i < size - 1 else "┘")
                )
                middle_intersection = (
                    "┬" if i == 0 else ("┼" if i < size - 1 else "┴")
                )

                # First intersection
                if j == 0:
                    line += first_intersection if intersection is None \
                          else str(intersection)
                # Last intersection
                elif j == size - 1:
                    line += last_intersection if intersection is None \
                          else str(intersection)
                # Middle intersections
                else:
                    line += middle_intersection if intersection is None \
                          else str(intersection)

                # Add horizontal separator for all intersections except last
                if j < size - 1:
                    line += "─"
            print(line)


    def get_move(self) -> tuple[int, int]:
        """
        See GoUI.get_move
        """
        move = None
        while move is None:
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
                    move = None
                    print(Fore.RED + "Invalid move. Please try again." +\
                            Style.RESET_ALL)
                    time.sleep(0.4)
            except ValueError:
                print(Fore.RED + "Invalid move. Please try again." +\
                               Style.RESET_ALL)
                time.sleep(0.4)
                move = None
        return move

def main() -> None:
    """
    Main TUI event loop
    """
    os.system("clear")
    # Welcome message
    _ = input(Fore.GREEN + ">>WELCOME TO 碁! PRESS ANY KEY TO START<<\n"\
                    + Style.RESET_ALL)
    os.system("clear")
    side = int(sys.argv[1])
    go = GoFake(side, 2)
    go_tui = GoTUI(go)

    go_tui.display_board()
    while True:
        if go.done:
            time.sleep(0.4)
            print(Fore.GREEN + "Game is over")
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.4)
            if len(go.outcome) > 1:
                print(f"It's a {Fore.CYAN}tie{Fore.GREEN}! ({go.scores()[1]} vs\
                    {go.scores()[2]}){Style.RESET_ALL}")
            else:
                print(f"Player {go.outcome[0]} wins! ({go.scores()[1]} vs\
                    {go.scores()[2]})")
            sys.exit(0)
        move = go_tui.get_move()
        if move is None:
            go.pass_turn()
        else:
            go.apply_move(move)
        os.system("clear")
        go_tui.display_board()


if __name__ == "__main__":
    main()

"""
TUI implementation for GoStub
"""
import sys

from fakes import GoStub
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
        for i, row in enumerate(self._go_game.grid):
            

#   1 2 3 4 5 6 7 8 9
#9 ●─┬─┬─┬─┬─┬─┬─┬─○
#8 ├─┼─┼─┼─┼─┼─┼─┼─┤
#7 ├─┼─┼─┼─┼─┼─┼─┼─┤
#6 ├─┼─┼─┼─┼─┼─┼─┼─┤
#5 ├─┼─┼─┼─┼─┼─┼─┼─┤
#4 ┼─┼─┼─┼─┼─┼─┼─┼─┤
#3 ├─┼─┼─┼─┼─┼─┼─┼─┤
#2 ├─┼─┼─┼─┼─┼─┼─┼─┤
#1 └─┴─┴─┴─┴─┴─┴─┴─┘

    def get_move(self) -> tuple[int, int]:
        """
        See GoUI.get_move
        """
        # ! TODO (not required for milestone 1)

def main():
    """
    Main TUI loop
    """
    side = int(sys.argv[1])
    go = GoStub(side, 2, False)
    go_tui = GoTUI(go)
    go_tui.display_board()
    # ! TODO for milestone 1: IMPLEMENT BASIC EVENT LOOP

if __name__ == "__main__":
    main()

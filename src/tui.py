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
        board = self._go_game.grid
        for i, row in enumerate(board):
            line = ""
            for j, intersection in enumerate(row):
                if j == 0:
                    if i == 0:
                        line += "┌" if intersection is None else str(intersection)
                    elif i < size - 1:
                        line += "├" if intersection is None else str(intersection)
                    else:
                        line += "└" if intersection is None else str(intersection)
                elif j == size - 1:
                    if i == 0:
                        line += "┐" if intersection is None else str(intersection)
                    elif i < size - 1:
                        line += "┤" if intersection is None else str(intersection)
                    else:
                        line += "┘" if intersection is None else str(intersection)
                else:
                    if i == 0:
                        line += "┬" if intersection is None else str(intersection)
                    elif i < size - 1:
                        line += "┼" if intersection is None else str(intersection)
                    else:
                        line += "┴" if intersection is None else str(intersection)
                if j < size -1:
                    line += "─"
            print(line)

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

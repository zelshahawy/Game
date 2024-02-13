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

        # First row
        first_row = ""
        for i, intersection in enumerate(board[0]):
            if i == 0:
                first_row += "┌" if intersection is None else str(intersection) + "─"
            elif intersection is None:
                first_row += "┬─"
            elif intersection is not None:
                first_row += str(intersection)
            elif i == size - 1:
                first_row += "┐" if intersection is None else str(intersection)
        print(first_row)

        # Middle rows
        for row in board[1:-1]:
            disp_row = ""
            for i, intersection in enumerate(row):
                if i == 0:
                    disp_row += "├─" if intersection is None else str(intersection) + "─"
                elif i < size - 1 and intersection is None:
                    disp_row += "┼─"
                elif i < size - 1 and intersection is not None:
                    disp_row += str(intersection) + "─"
                elif i == size - 1:
                    disp_row += "┤" if intersection is None else str(intersection)
            print(disp_row)

        # Final row
        last_row = ""
        for i, intersection in enumerate(board[-1]):
            if i == 0:
                last_row += "└" if intersection is None else str(intersection) + "─"
            elif intersection is None:
                last_row += "┴─"
            elif intersection is not None:
                last_row += str(intersection)
            elif i == size - 1:
                last_row += "┘" if intersection is None else str(intersection)
        print(last_row)

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

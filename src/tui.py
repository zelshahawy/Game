"""
TUI implementation for GoStub
"""
import sys
import os

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
            for j, intx in enumerate(row):
                # First intx
                if j == 0:
                    if i == 0:
                        line += "┌" if intx is None else str(intx)
                    elif i < size - 1:
                        line += "├" if intx is None else str(intx)
                    else:
                        line += "└" if intx is None else str(intx)
                # Last intx
                elif j == size - 1:
                    if i == 0:
                        line += "┐" if intx is None else str(intx)
                    elif i < size - 1:
                        line += "┤" if intx is None else str(intx)
                    else:
                        line += "┘" if intx is None else str(intx)
                # Middle intxs
                else:
                    if i == 0:
                        line += "┬" if intx is None else str(intx)
                    elif i < size - 1:
                        line += "┼" if intx is None else str(intx)
                    else:
                        line += "┴" if intx is None else str(intx)
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
            move_input = input("ENTER MOVE (X Y) ")
            try:
                coordinates = move_input.split()
                if len(coordinates) != 2:
                    print("INVALID INPUT")
                else:
                    move = (int(coordinates[0]), int(coordinates[1]))
                if not self._go_game.legal_move(move):
                    print("INVALID INPUT")
                    move = None
            except ValueError:
                print("INVALID INPUT")
        return move


def main():
    """
    Main TUI loop
    """
    side = int(sys.argv[1])
    go = GoStub(side, 2, False)
    go_tui = GoTUI(go)
    go_tui.display_board()
    while True:
        move = go_tui.get_move()
        go.apply_move(move)
        os.system("clear")
        go_tui.display_board()


if __name__ == "__main__":
    main()

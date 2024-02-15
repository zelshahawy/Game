"""
GUI implementation for Go stub
"""

import sys
from typing import Optional
import pygame
from fakes import GoStub
from ui import GoUI


BOARD_SIZE = int(sys.argv[1])

CELL_SIZE = 600 // BOARD_SIZE
PLAYER_STONE_RADIUS = CELL_SIZE // 3
BOARD_PADDING = 20
WIDTH_DISPLAY = BOARD_SIZE * CELL_SIZE

REFRESH_RATE = 24

BLACK = (0, 0, 0)
ORANGE = (230, 165, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

class GoGUI(GoUI):
    """
    Graphical version class for GoUI
    """

    buttons: dict[str, tuple[int, int]]
    screen: pygame.surface.Surface
    clock_timer: pygame.time.Clock
    board_padding : int

    def __init__(self, go_game : GoStub) -> None:
        super().__init__(go_game)

        pygame.init()
        self.clock_timer= pygame.time.Clock()


        pygame.display.set_caption("GoGUI")
        self.screen = pygame.display.set_mode(
            (WIDTH_DISPLAY+50, WIDTH_DISPLAY+50 )
        )

    def display_board(self) -> None:
        """
        See GoUI.display_board
        """
        self.screen.fill(ORANGE)

        for i in range(0, BOARD_SIZE):
            start_hori = (BOARD_PADDING, i * CELL_SIZE + BOARD_PADDING)
            end_hori = ((BOARD_SIZE - 1) * CELL_SIZE + BOARD_PADDING,\
                i * CELL_SIZE + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_hori, end_hori,3)

            start_vert = (i * CELL_SIZE + BOARD_PADDING, BOARD_PADDING)
            end_vert = (i * CELL_SIZE + BOARD_PADDING,\
                (BOARD_SIZE - 1) * CELL_SIZE + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_vert, end_vert, 3)

    def get_move(self) -> tuple[int, int]:
        """
        See GoUI.get_move
        """
        raise NotImplementedError

    def on_click(self, pos_click : tuple[int, int]) -> None:
        """
        Handles interactions with the GUI
        """
        print(pos_click)

    def draw_player_stone(self, num_player : Optional[int], board_pos : \
        Optional[tuple[int,int]]) -> None:
        """
        Draws a specific player stone on the board
        """
        if board_pos is None or num_player is None:
            return
        x, y = board_pos

        stone_x = x * CELL_SIZE + BOARD_PADDING
        stone_y = y * CELL_SIZE + BOARD_PADDING

        if num_player == 1:
            pygame.draw.circle(self.screen, WHITE, (stone_x, stone_y),\
            PLAYER_STONE_RADIUS)
        elif num_player == 2:
            pygame.draw.circle(self.screen, BLACK, (stone_x, stone_y),\
            PLAYER_STONE_RADIUS)

    def draw_board_state(self) -> None:
        """
        Draws all stones on board 
        """
        grid_state = self._go_game.grid

        for i, _ in enumerate(grid_state):
            for j, _ in enumerate(grid_state[i]):
                piece_at_pos = self._go_game.piece_at((i, j))
                self.draw_player_stone(piece_at_pos, (i, j))

    def draw_window(self) -> None:
        """Displays window"""
        self.display_board()
        self.draw_board_state()

    def gui_loop(self) -> None:
        """
        Handles display of change in game state, position, and players'moves
        """
        while True:
            py_events = pygame.event.get()
            for event in py_events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event.pos)

            self.draw_window()
            pygame.display.update()
            self.clock_timer.tick(REFRESH_RATE)


if __name__ == "__main__":
    go = GoStub(BOARD_SIZE, 2, False)
    goGUI = GoGUI(go)
    goGUI.gui_loop()

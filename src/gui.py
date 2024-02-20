"""
GUI implementation for Go stub
"""

import sys
from typing import Optional
import pygame
from fakes import GoFake
from ui import GoUI


BOARD_SIZE = int(sys.argv[1])

CELL_SIZE = 700 // BOARD_SIZE
PLAYER_STONE_RADIUS = CELL_SIZE // 4
BOARD_PADDING = 100
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
    all_pos : dict[tuple[int,int], tuple[int,int]]
    FONT : pygame.font.Font

    def __init__(self, go_game: GoFake) -> None:
        super().__init__(go_game)

        pygame.init()
        self.clock_timer= pygame.time.Clock()
        self.all_pos = {}

        self.button_pass_rect = pygame.Rect(5, WIDTH_DISPLAY//2, 50, 30)

        self.FONT = pygame.font.SysFont("Arial", 25)

        pygame.display.set_caption("GoGUI")
        self.screen = pygame.display.set_mode(
            (WIDTH_DISPLAY+BOARD_PADDING, WIDTH_DISPLAY+BOARD_PADDING)
        )

    def display_board(self) -> None:
        """
        See GoUI.display_board
        """
        self.screen.fill(ORANGE)

        pygame.draw.rect(self.screen, WHITE, self.button_pass_rect)

        for i in range(0, BOARD_SIZE):
            start_hori = (BOARD_PADDING, i * CELL_SIZE + BOARD_PADDING)
            end_hori = ((BOARD_SIZE - 1) * CELL_SIZE + BOARD_PADDING,\
                i * CELL_SIZE + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_hori, end_hori, 3)

            start_vert = (i * CELL_SIZE + BOARD_PADDING, BOARD_PADDING)
            end_vert = (i * CELL_SIZE + BOARD_PADDING,\
                (BOARD_SIZE - 1) * CELL_SIZE + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_vert, end_vert, 3)

    def get_move(self) -> tuple[int, int]:
        """
        See GoUI.get_move
        """
        return (0, 0)

    def _on_click(self, pos_click: tuple[int, int]) -> None:
        """
        Handles interactions with the GUI
        """

        if self.button_pass_rect.collidepoint(pos_click):
            self._go.pass_turn()
            return

        x_click, y_click = pos_click

        for board_pos, center_coord in self.all_pos.items():
            x_center, y_center = center_coord
            euclid_sq = (x_click - x_center ) ** 2 + (y_click - y_center) ** 2
            euclid_dist = euclid_sq ** 0.5

            if euclid_dist <= PLAYER_STONE_RADIUS:
                self._go.apply_move(board_pos)

    def _draw_button(self, rect, text):
        """
        Draws the pass button
        """
        pygame.draw.rect(self.screen, WHITE, rect)

        if text:
            text_surf = self.FONT.render(text, True, BLACK)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

    def _draw_player_stone(self, num_player: Optional[int], board_pos: \
        Optional[tuple[int,int]]) -> None:
        """
        Draws a specific player stone on the board

        For empty positions, a circle indicator is shown around the nearest
        line intersection to guide player where to click on next
        """
        if board_pos is None:
            return
        x, y = board_pos

        stone_x = x * CELL_SIZE + BOARD_PADDING
        stone_y = y * CELL_SIZE + BOARD_PADDING

        self.all_pos[(x,y)] = (stone_x, stone_y)

        if num_player == 1:
            pygame.draw.circle(
                self.screen,
                WHITE,
                (stone_x, stone_y),
                PLAYER_STONE_RADIUS
            )
        elif num_player == 2:
            pygame.draw.circle(
                self.screen,
                BLACK,
                (stone_x, stone_y),
                PLAYER_STONE_RADIUS
            )
        elif num_player is None:
            self._hover_board_pos(pygame.mouse.get_pos())

    def _hover_board_pos(self, pos_hover: tuple[int,int]) -> None:
        """
        Highlights a position on the board where a player can click to 
        play his turn

        Args : pos_hover (tuple[int,int]) -  the position where the mouse is 
            hovering over the screen
        """

        x_hover, y_hover = pos_hover

        for center_coord in self.all_pos.values():
            x_center, y_center = center_coord
            euclid_sq = (x_hover - x_center )**2 + (y_hover - y_center)**2
            euclid_dist = euclid_sq**0.5

            if euclid_dist <= PLAYER_STONE_RADIUS:

                pygame.draw.circle(
                self.screen,
                GREY,
                (x_center, y_center),
                PLAYER_STONE_RADIUS,
                width = 1)

                return

    def display_texts(self) -> None:
        """
        Displays important information such as current player turn, final winner
        and scores
        """
        if self._go.done:
            winner = self._go.outcome

            text = f" The winner(s) is(are) {winner} \
            Game Scores : {self._go.scores()}"
        else:
            text = f" Current turn: Player {self._go.turn}" + \
            f"  Game Scores : {self._go.scores()}"

        img = self.FONT.render(text, True, BLACK)

        self.screen.blit(img, (WIDTH_DISPLAY//4 , 30))


    def _draw_board_state(self) -> None:
        """
        Draws all stones on board 
        """
        grid_state = self._go.grid

        for i, _ in enumerate(grid_state):
            for j, _ in enumerate(grid_state[i]):
                piece_at_pos = self._go.piece_at((i, j))
                self._draw_player_stone(piece_at_pos, (i, j))

    def _draw_window(self) -> None:
        """
        Displays window
        """
        self.display_board()
        self._draw_button(self.button_pass_rect, "PASS")
        self.display_texts()
        self._draw_board_state()

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

                elif self._go.done:
                    continue

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._on_click(event.pos)

            self._draw_window()
            pygame.display.update()
            self.clock_timer.tick(REFRESH_RATE)

if __name__ == "__main__":
    go = GoFake(BOARD_SIZE, 2, False)
    goGUI = GoGUI(go)
    goGUI.gui_loop()

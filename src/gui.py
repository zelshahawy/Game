"""
GUI implementation for Go stub
"""

import sys
from typing import Optional
import pygame
from fakes import GoFake
from go import Go


BOARD_SIZE = int(sys.argv[1])

CELL_SIZE = 700 // BOARD_SIZE
PLAYER_STONE_RADIUS = CELL_SIZE // 4
BOARD_PADDING = 100
WIDTH_DISPLAY = BOARD_SIZE * CELL_SIZE

REFRESH_RATE = 24

ORANGE = (230, 165, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)



PLAYER_COLORS = [0, BLACK, WHITE, BLUE, PURPLE, RED, GREEN, MAGENTA, CYAN, GREY]
class GoGUI():
    """
    Graphical version class for GoUI
    """
    go: GoFake
    buttons: dict[str, tuple[int, int]]
    screen: pygame.surface.Surface
    clock_timer: pygame.time.Clock
    board_padding: int
    all_pos: dict[tuple[int,int], tuple[int,int]]
    FONT: pygame.font.Font
    game_started : bool

    def __init__(self, go: Go) -> None:
        """
        Constructor

        Args:
            go: The Go game to display and interact with
        """
        self._go = go

        pygame.init()
        self.game_started = False
        self.clock_timer= pygame.time.Clock()
        self.all_pos = {}
        self.player_colors = { player_int : PLAYER_COLORS[player_int] for\
        player_int in range(1, go.num_players + 1)}

        self.button_pass_rect = pygame.Rect(5, WIDTH_DISPLAY//2, 50, 30)
        self. button_start_rect = pygame.Rect(WIDTH_DISPLAY//2 - 50,\
        WIDTH_DISPLAY//2 + 100, 200, 50)

        self.FONT = pygame.font.SysFont("Arial", 25)

        pygame.display.set_caption("GoGUI")
        self.screen = pygame.display.set_mode(
            (WIDTH_DISPLAY+BOARD_PADDING, WIDTH_DISPLAY+BOARD_PADDING)
        )

    def display_board(self) -> None:
        """
        Displays the current state of the board in the GUI

        Returns: nothing
        """
        for i in range(0, BOARD_SIZE):
            start_hori = (BOARD_PADDING, i * CELL_SIZE + BOARD_PADDING)
            end_hori = ((BOARD_SIZE - 1) * CELL_SIZE + BOARD_PADDING,\
                i * CELL_SIZE + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_hori, end_hori, 3)

            start_vert = (i * CELL_SIZE + BOARD_PADDING, BOARD_PADDING)
            end_vert = (i * CELL_SIZE + BOARD_PADDING,\
                (BOARD_SIZE - 1) * CELL_SIZE + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_vert, end_vert, 3)

    def _on_click(self, pos_click: tuple[int, int]) -> None:
        """
        Handles interactions with the GUI
        """

        if self.button_pass_rect.collidepoint(pos_click):
            self._go.pass_turn()
            return
        elif self.button_start_rect.collidepoint(pos_click):
            self. button_start_rect = pygame.Rect(0,0,0,0)
            self.game_started = True
            return

        x_click, y_click = pos_click

        for board_pos, center_coord in self.all_pos.items():
            x_center, y_center = center_coord
            euclid_sq = (x_click - x_center ) ** 2 + (y_click - y_center) ** 2
            euclid_dist = euclid_sq ** 0.5

            if euclid_dist <= PLAYER_STONE_RADIUS and \
            self._go.legal_move(board_pos):
                self._go.apply_move(board_pos)

    def _draw_button(self, font : pygame.font.Font, rect: \
        pygame.rect.Rect, text: str) -> None:
        """
        Draws the pass button
        """
        pygame.draw.rect(self.screen, WHITE, rect)

        if text:
            text_surf = font.render(text, True, BLACK)
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

        if num_player:
            pygame.draw.circle(
                self.screen,
                self.player_colors[num_player],
                (stone_x, stone_y),
                PLAYER_STONE_RADIUS)

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

    def display_texts(self, text : str, font : pygame.font.Font, pos_text : \
        tuple[int, int] = (BOARD_SIZE , 30)) -> None:
        """
        Displays important information such as current player turn, final winner
        and scores
        """
        img = font.render(text, True, BLACK)
        self.screen.blit(img, pos_text)

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
        self.screen.fill(ORANGE)

        if self.game_started:
            self.display_board()           
            self._draw_button(self.FONT, self.button_pass_rect, "PASS")
            self._draw_board_state()

            if self._go.done:
                winner = self._go.outcome

                text = f" The winner(s) is(are) {winner} " + \
                f" Game Scores : {self._go.scores()}"
            else:
                text = f" Current turn: Player {self._go.turn} " + \
                f" Game Scores : {self._go.scores()}"
                self._draw_player_stone(self._go.turn, (-1, -1))

            self.display_texts(text,self.FONT)

        else:
            START_FONT = pygame.font.SysFont("Arial", 40)
            GO_FONT = pygame.font.SysFont("Arial", 100)

            self.display_texts("GO",GO_FONT, \
            (WIDTH_DISPLAY//2, WIDTH_DISPLAY//2))
            self._draw_button(START_FONT, self.button_start_rect,"START GAME")


    def gui_loop(self) -> None:
        """
        Handles display of change in game state, position, and players'moves
        """
        loop = True
        while loop:
            py_events = pygame.event.get()
            for event in py_events:
                if event.type == pygame.QUIT:
                    loop = False
                    sys.exit()

                elif self._go.done:
                    continue

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._on_click(event.pos)

            self._draw_window()
            pygame.display.update()
            self.clock_timer.tick(REFRESH_RATE)
    
        pygame.quit()

def play_sound(sound_path):
    """
    given a path to a an audio file, plays it.
    """
    my_sound_mixer = pygame.mixer
    my_sound_mixer.init()
    my_sound = my_sound_mixer.Sound(sound_path)
    my_sound.set_volume(1.0)
    my_sound.play(-1)

if __name__ == "__main__":
    play_sound("src/bgm")
    go = Go(19,9)
    goGUI = GoGUI(go)
    goGUI.gui_loop()

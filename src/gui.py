"""
GUI implementation for Go
"""
import math
import sys
from typing import Optional
import click
import pygame
from go import Go

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
    go: Go
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
        self.captured_pos_color = {}
        self.player_colors = { player_int : PLAYER_COLORS[player_int] for\
        player_int in range(1, go.num_players + 1)}

        self.BOARD_SIZE = go.size
        self.CELL_SIZE = 700 // self.BOARD_SIZE
        self.PLAYER_STONE_RADIUS = self.CELL_SIZE // 4
        self.BOARD_PADDING = 100
        self.WIDTH_DISPLAY = self.BOARD_SIZE * self.CELL_SIZE
        self.REFRESH_RATE = 24

        self.button_pass_rect = pygame.Rect(5, self.WIDTH_DISPLAY//2, 50, 30)
        self. button_start_rect = pygame.Rect(self.WIDTH_DISPLAY//2 - 50,\
        self.WIDTH_DISPLAY//2 + 100, 200, 50)

        self.FONT = pygame.font.SysFont("Arial", 25)

        pygame.display.set_caption("GoGUI")
        self.screen = pygame.display.set_mode(
            (self.WIDTH_DISPLAY + self.BOARD_PADDING, self.WIDTH_DISPLAY + \
            self.BOARD_PADDING)
        )

    def display_board(self) -> None:
        """
        Displays the current state of the board in the GUI
        """

        for i in range(0, self.BOARD_SIZE):
            start_hori = (self.BOARD_PADDING, i * self.CELL_SIZE + \
            self.BOARD_PADDING)
            end_hori = ((self.BOARD_SIZE - 1) * self.CELL_SIZE + \
            self.BOARD_PADDING, i * self.CELL_SIZE + self.BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_hori, end_hori, 3)

            start_vert = (i * self.CELL_SIZE + self.BOARD_PADDING, \
            self.BOARD_PADDING)
            end_vert = (i * self.CELL_SIZE + self.BOARD_PADDING,\
            (self.BOARD_SIZE - 1) * self.CELL_SIZE + self.BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_vert, end_vert, 3)

    def _on_click(self, pos_click: tuple[int, int]) -> None:
        """
        Handles click interactions with the GUI
            Args: 
                pos_click (tuple[int, int]) -  the position on the pygame
                display window where the click occured
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

            if euclid_dist <= self.PLAYER_STONE_RADIUS and \
            self._go.legal_move(board_pos):
                self.captured_pos_color = self._go.captured_pos_color
                self._go.apply_move(board_pos)

    def _draw_button(self, font: pygame.font.Font, rect: \
        pygame.rect.Rect, text: str) -> None:
        """
        Draws pygame button with specidied font and rectangle params
            Args:
                font (pygame.font.Font) - font style on the buttons text
                rect (pygame.rect.Rect) - rectangle parameters where the button
                will be positioned in the window display
                text (str) - the call to action text to be displayed on the
                button
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

            Args:
                num_player (int|None) - the nth player's turn
                board_pos (tuple[int, int]|None) - the position on the board to
                draw all stones on the board or an outline of the position one
                can place the next stone
        """
        x, y = board_pos

        stone_x = x * self.CELL_SIZE + self.BOARD_PADDING
        stone_y = y * self.CELL_SIZE + self.BOARD_PADDING

        self.all_pos[(x,y)] = (stone_x, stone_y)

        if board_pos in self.captured_pos_color and num_player is None:
            arc_rect = self.PLAYER_STONE_RADIUS//2
            player_num_captured = self.captured_pos_color[board_pos]

            start_angle = 0 
            end_angle = 360  
            while end_angle > 0: 
                end_angle -= 20
                start_angle_rad = math.radians(start_angle)
                end_angle_rad = math.radians(end_angle)

                pygame.draw.arc(
                    self.screen,
                    self.player_colors[player_num_captured],
                    (stone_x, stone_y, self.CELL_SIZE, self.CELL_SIZE), 
                    start_angle_rad,
                    end_angle_rad,
                    arc_rect  
                )

            del self.captured_pos_color[board_pos]

        if num_player:
            pygame.draw.circle(
                self.screen,
                self.player_colors[num_player],
                (stone_x, stone_y),
                self.PLAYER_STONE_RADIUS)

        elif num_player is None and not self._go.done:
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

            if euclid_dist <= self.PLAYER_STONE_RADIUS:

                pygame.draw.circle(
                self.screen,
                GREY,
                (x_center, y_center),
                self.PLAYER_STONE_RADIUS,
                width = 1)

                return

    def display_texts(self, text: str, font: pygame.font.Font, pos_text: \
        tuple[int, int] = (20, 30)) -> None:
        """
        Displays important information such as current player turn, final winner
        and scores
            Args:
                text (str) - the text to be displayed
                font (pygame.font.Font) - font style on the buttons text
                pos_text (tuple[int, int]) -  the position on the pygame window
                where the text will be rendered
        """
        img = font.render(text, True, BLACK)
        self.screen.blit(img, pos_text)

    def _draw_board_state(self) -> None:
        """
        Draws all stones on board to represent the current state of the board
        """
        grid_state = self._go.grid

        for i, _ in enumerate(grid_state):
            for j, _ in enumerate(grid_state[i]):
                piece_at_pos = self._go.piece_at((i, j))
                self._draw_player_stone(piece_at_pos, (i, j))
 
    def _draw_window(self) -> None:
        """
        Displays pygame's interactive window
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

            self.display_texts(text,self.FONT)

        else:
            START_FONT = pygame.font.SysFont("Arial", 40)
            GO_FONT = pygame.font.SysFont("Arial", 100)

            self.display_texts("GO",GO_FONT, \
            (self.WIDTH_DISPLAY//2, self.WIDTH_DISPLAY//2))
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
                    pygame.quit()
                    sys.exit()

                elif self._go.done:
                    continue

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._on_click(event.pos)

            self._draw_window()
            pygame.display.update()
            self.clock_timer.tick(self.REFRESH_RATE)

@click.command()
@click.option("-n", "--num-players", default=2, help="Number of players")
@click.option("-s", "--size", default=19, help="Size of the board")
@click.option("--simple-ko", is_flag=True, help="Use simple ko rule")
@click.option("--super-ko", is_flag=True, help="Use super ko rule")
def create_game(num_players: int , size: int, simple_ko : bool, super_ko: bool)\
    -> None:
    """
    Creates go game from click commands, initializes GUI
        Args:
            num_players (int) -  the number of players in go
            size (int) -  size of go board to be used
            simple_ko (bool) - property that sets the simple_ko rule if super_ko
            is not declared in click interface
            super_ko - property that sets super_ko rule
    """
    go = Go(size, num_players, super_ko)
    goGUI = GoGUI(go)
    goGUI.gui_loop()

def play_sound(sound_path : any) -> None:
    """
    given a path to a an audio file, plays it.
    """
    my_sound_mixer = pygame.mixer
    my_sound_mixer.init()
    my_sound = my_sound_mixer.Sound(sound_path)
    my_sound.set_volume(1.0)
    my_sound.play(-1)

if __name__ == "__main__":
    play_sound("src/data/bgm")
    create_game()

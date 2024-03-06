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

PLAYER_COLORS = [WHITE, BLACK, BLUE, PURPLE, RED, GREEN, MAGENTA, CYAN, GREY]
BOARD_PADDING = 100

class GoGUI():
    """
    Class for presenting GUI for a game of Go
    """
    go: Go
    screen: pygame.surface.Surface
    clock_timer: pygame.time.Clock
    all_pos: dict[tuple[int,int], tuple[int,int]]
    game_started : bool
    captured_pos_color : dict[tuple[int,int], int | None]
    cell_size : int
    stone_rad : int
    buttons : dict[str, pygame.rect.Rect]

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

        self.cell_size = 700 // self._go.size
        self.stone_rad = self.cell_size // 4

        display_width = self._go.size * self.cell_size
        self.buttons = \
        {"pass_rect" : pygame.rect.Rect(5, display_width//2, 50, 30),\
        "start_rect" :pygame.rect.Rect(display_width//2 - 50,\
        display_width//2 + 50, 200, 50)}

        pygame.display.set_caption("GoGUI")
        self.screen = pygame.display.set_mode(
        (display_width + BOARD_PADDING, display_width + BOARD_PADDING))

    def display_board(self) -> None:
        """
        Displays the current state of the board in the GUI
        """

        for i in range(0, self._go.size):
            start_hori = (BOARD_PADDING, i * self.cell_size + \
            BOARD_PADDING)
            end_hori = ((self._go.size - 1) * self.cell_size + \
            BOARD_PADDING, i * self.cell_size + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_hori, end_hori, 3)

            start_vert = (i * self.cell_size + BOARD_PADDING, \
            BOARD_PADDING)
            end_vert = (i * self.cell_size + BOARD_PADDING,\
            (self._go.size - 1) * self.cell_size + BOARD_PADDING)
            pygame.draw.aaline(self.screen, GREY, start_vert, end_vert, 3)

    def _on_click(self, pos_click: tuple[int, int]) -> None:
        """
        Handles click interactions with the GUI
            Args: 
                pos_click (tuple[int, int]) -  the position on the pygame
                display window where the click occured
        """

        if self.buttons["pass_rect"].collidepoint(pos_click):
            self._go.pass_turn()
            return

        if self.buttons["start_rect"].collidepoint(pos_click):
            self.buttons["start_rect"] = pygame.rect.Rect(0,0,0,0)
            self.game_started = True
            return

        x_click, y_click = pos_click

        for board_pos, center_coord in self.all_pos.items():
            x_center, y_center = center_coord
            euclid_sq = (x_click - x_center ) ** 2 + (y_click - y_center) ** 2
            euclid_dist = euclid_sq ** 0.5

            if euclid_dist <= self.stone_rad and \
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
        Optional[tuple[int, int]]) -> None:
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
        if board_pos is not None:
            x, y = board_pos

        stone_x = x * self.cell_size + BOARD_PADDING
        stone_y = y * self.cell_size + BOARD_PADDING

        self.all_pos[(x,y)] = (stone_x, stone_y)

        if board_pos in self.captured_pos_color and num_player is None:
            self.animate_captured(board_pos, (stone_x, stone_y))

        if num_player:
            pygame.draw.circle(
                self.screen,
                PLAYER_COLORS[num_player - 1],
                (stone_x, stone_y),
                self.stone_rad)

        elif num_player is None and not self._go.done:
            self._hover_board_pos(pygame.mouse.get_pos())
    
    def animate_captured(self, board_pos :tuple[int, int],\
        display_pos : tuple[int,int]) -> None:
        """
        Animates the capture of stones into the centre of the cell as
        an arc that grows smaller and eventually disappears
        
        Args:
            board_pos (tuple[int, int]|None) - the position on the board to
            capture
            display_pos (tuple[int, int]) - the position on the pygame surface 
            to start the animation
        """
        stone_x, stone_y = display_pos
        arc_rect = self.stone_rad//2
        player_num_captured = self.captured_pos_color[board_pos]
        start_angle = 0
        end_angle = 360
        assert isinstance(player_num_captured, int)

        while end_angle > 0:
            end_angle -= 20
            start_angle_rad = math.radians(start_angle)
            end_angle_rad = math.radians(end_angle)
            pygame.draw.arc(
                self.screen,
                PLAYER_COLORS[player_num_captured - 1],
                (stone_x, stone_y, self.cell_size, self.cell_size),
                start_angle_rad,
                end_angle_rad,
                arc_rect)
        del self.captured_pos_color[board_pos]

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

            if euclid_dist <= self.stone_rad:

                pygame.draw.circle(
                self.screen,
                GREY,
                (x_center, y_center),
                self.stone_rad,
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
        font = pygame.font.SysFont("Arial", 18)

        if self.game_started:
            self.display_board()
            self._draw_button(font, self.buttons["pass_rect"], "PASS")
            self._draw_board_state()

            if self._go.done:
                winner = self._go.outcome

                text = f" The winner(s) is(are) {winner} " + \
                f" Game Scores : {self._go.scores()}"
            else:
                text = f" Current turn: Player {self._go.turn} " + \
                f" Game Scores : {self._go.scores()}"

            self.display_texts(text,font)

        else:
            start_font = pygame.font.SysFont("Arial", 20)
            go_font = pygame.font.SysFont("Arial", 50)
            disp_width = self._go.size * self.cell_size

            self.display_texts("GO",go_font, \
            (disp_width//2 + 20, disp_width//2))
            self._draw_button(start_font, self.buttons["start_rect"],\
            "START GAME")

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
            self.clock_timer.tick(24)

@click.command()
@click.option("-n", "--num-players", default=2, help="Number of players")
@click.option("-s", "--size", default=19, help="Size of the board")
@click.option("--simple-ko", is_flag=True, help="Use simple ko rule")
@click.option("--super-ko", is_flag=True, help="Use super ko rule")
def create_game(num_players: int = 2 , size: int = 19, simple_ko : bool = True,\
    super_ko: bool = False) -> None:
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
    go_gui = GoGUI(go)
    go_gui.gui_loop()

def play_sound(sound_path: str) -> None:
    """
    Given a path to a an audio file, plays it.
    """
    my_sound_mixer = pygame.mixer
    my_sound_mixer.init()
    my_sound = my_sound_mixer.Sound(sound_path)
    my_sound.set_volume(1.0)
    my_sound.play(-1)

def main() -> None:
    """
    Main function for running GUI
    """
    play_sound("src/data/bgm")
    create_game()

if __name__ == "__main__":
    main()

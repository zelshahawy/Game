"""
Fake implementations of GoBase.

We provide a GoStub implementation, and you must
implement a GoFake implementation.
"""
from copy import deepcopy
from base import GoBase, BoardGridType, ListMovesType


class GoStub(GoBase):
    """
    Stub implementation of GoBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.

    - The board is always initialized with four pieces in the four
      corners of the board. Player 1 has pieces in the northeast and
      southwest corners of the board, and Player 2 has pieces in the
      southeast and northwest corners of the board.
    - Players are allowed to place pieces in any position of the board
      they want, even if there is already a piece in that position
      (placing a piece in such a position replaces the previous piece
      with the new one). The ko and superko rule do not apply.
    - The game ends after four moves. Whatever player has a piece in
      position (0,1) wins. If there is no piece in that position,
      the game ends in a tie.
    - The scores are always reported as 100 for Player 1 and 200 for
      Player 2. Note how the scores do not play a role in determining
      the outcome of the game.
    - It does not validate board positions. If a method is called with
      a position outside the board, the method will likely cause an exception.
    - It does not implement the load_game or simulate_moves method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, superko: bool = False):
        """
        See GoBase.__init__
        """
        if players != 2:
            raise ValueError(
                "The stub implementation ", "only supports two players"
            )

        super().__init__(side, players, superko)

        self._grid = [[None] * side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        """
        See GoBase.grid
        """
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        See GoBase.turn
        """
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        """
        See GoBase.available_moves
        """
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        """
        See GoBase.done
        """
        return self._num_moves == 4

    @property
    def outcome(self) -> list[int]:
        """
        See GoBase.outcome
        """
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [1, 2]
        return [self._grid[0][1]]

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        """
        See GoBase.piece_at
        """
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        See GoBase.legal_move
        """
        return True

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        See GoBase.apply_move
        """
        r, c = pos
        self._grid[r][c] = self._turn
        self.pass_turn()

    def pass_turn(self) -> None:
        """
        See GoBase.pass_turn
        """
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def scores(self) -> dict[int, int]:
        """
        See GoBase.scores
        """
        return {1: 100, 2: 200}

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        See GoBase.load_game
        """
        raise NotImplementedError

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        """
        See GoBase.simulate_move
        """
        raise NotImplementedError

#
# Your GoFake implementation goes here
#
class GoFake(GoBase):
    """
    Fake implementation of GoBase

    _previous_boards: BoardGridType
    _previous_board: BoardGridType
    _consecutive_passes: int

    """
    def __init__(self, side: int, players: int, superko: bool = False):
        """
        See GoBase.__init__
        """
        if players != 2:
            raise ValueError(
                "The fake implementation only supports two players"
            )

        if side < 4:
            raise ValueError(
                "The fake implementation only supports boards of "+
                "size 4x4 and above"
            )

        super().__init__(side, players, superko)

        self._grid: BoardGridType = [[None] * side for _ in range(side)]

        self._turn = 1
        self._num_moves = 0
        self._consecutive_passes = 0

        if self._superko:
            self._previous_boards: list[BoardGridType] = []
        else:
            self._previous_board: BoardGridType | None = None

    @property
    def num_moves(self) -> int:
        """
        Returns the number of moves
        """
        return self._num_moves

    @property
    def grid(self) -> BoardGridType:
        """
        See GoBase.grid
        """
        return deepcopy(self._grid)

    @property
    def game_turn(self) -> int:
        """
        returns number of turns in a game
        """
        return self._num_moves

    @grid.setter
    def grid(self, new_grid: BoardGridType) -> None:
        """
        Sets the grid to a new grid

        Args:
            new_grid: new grid to set the grid to

        Returns: nothing
        """
        self._grid = new_grid

    @property
    def turn(self) -> int:
        """
        See GoBase.turn
        """
        return self._turn

    @turn.setter
    def turn(self, new_turn: int) -> None:
        """
        Sets the turn to a new turn

        Args:
            new_turn: new turn to set the turn to

        Returns: nothing
        """
        self._turn = new_turn

    @property
    def consecutive_passes(self) -> int:
        """
        Returns the number of consecutive passes
        """
        return self._consecutive_passes

    @consecutive_passes.setter
    def consecutive_passes(self, new_consecutive_passes: int) -> None:
        """
        Sets the consecutive passes to a new number

        Args:
            new_consecutive_passes: new number to set the consecutive passes to

        Returns: nothing
        """
        self._consecutive_passes = new_consecutive_passes

    @property
    def available_moves(self) -> ListMovesType:
        """
        See GoBase.available_moves
        """
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                if self.piece_at((r, c)) is None:
                    moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        """
        See GoBase.done
        """
        return (
            self._consecutive_passes == 2 or self.piece_at((0, 0)) is not None
        )

    @property
    def outcome(self) -> list[int]:
        """
        See GoBase.outcome
        """
        if not self.done:
            return []
        scores = self.scores()
        max_score = max(scores.values())
        winners = []
        for player, score in scores.items():
            if score == max_score:
                winners.append(player)
        return winners

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        """
        See GoBase.piece_at
        """
        if not self.in_bounds(pos):
            raise ValueError("Position is outside bounds of the board")

        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        See GoBase.legal_move
        """
        if pos is None:
            return True

        if not self.in_bounds(pos):
            raise ValueError("Move is outside bounds of the board")

        resulting_board = self.simulate_move(pos).grid

        if self._superko and resulting_board in self._previous_boards:
            return False
        if resulting_board == self._previous_board:
            return False

        if self.piece_at(pos) is not None:
            return False

        return True

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        See GoBase.apply_move
        """
        if self._superko:
            self._previous_boards.append((self.grid))
        else:
            self._previous_board = self.grid

        if not self.in_bounds(pos):
            raise ValueError("Move is outside bounds of the board")
        r, c = pos
        self._grid[r][c] = self._turn

        if pos == (0, 0):
            self.populate_positions()
            return

        for adj_pos in self.adjacent_positions(pos):
            if self.piece_at(adj_pos) is not None and \
            self.piece_at(adj_pos) != self.turn:
                self._grid[adj_pos[0]][adj_pos[1]] = None

        self.pass_turn()
        self._consecutive_passes = 0

    def populate_positions(self) -> None:
        """
        Populates all empty positions in board with the current player's pieces

        Returns: nothing
        """
        for r, c in self.available_moves:
            self._grid[r][c] = self._turn

    def in_bounds(self, pos: tuple[int, int]) -> bool:
        """
        Returns whether a position is inside the bounds of the board
        
        Args:
            pos: position to check

        Returns: whether the position is inside the bounds
        """
        r, c = pos
        return 0 <= r < self._side and 0 <= c < self._side

    def adjacent_positions(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Returns all positions adjacent to a given position

        Args:
            pos: position to check positions adjacent to

        Returns: list of all adjacent positions
        """
        pieces = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            potential_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if self.in_bounds(potential_pos):
                pieces.append(potential_pos)
        return pieces

    def pass_turn(self) -> None:
        """
        See GoBase.pass_turn
        """
        self._consecutive_passes += 1
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1


    def scores(self) -> dict[int, int]:
        """
        See GoBase.scores
        """
        p1_score = len(
            [piece for row in self.grid for piece in row if piece == 1]
        )
        p2_score = len(
            [piece for row in self.grid for piece in row if piece == 2]
        )

        return {1: p1_score, 2: p2_score}

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        See GoBase.load_game
        """
        raise NotImplementedError

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        """
        See GoBase.simulate_move
        """
        new_go = GoFake(self._side, self._players, self._superko)
        new_go.grid = self.grid
        new_go.turn = self.turn
        new_go.consecutive_passes = self._consecutive_passes

        if pos is not None:
            if not self.in_bounds(pos):
                raise ValueError("Position is outside the bounds of the board")

            new_go.apply_move(pos)
        else:
            new_go.pass_turn()

        return new_go

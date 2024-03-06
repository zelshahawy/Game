"""
Tests for Go
"""
import pytest
from go import Go
from typing import Union

####Fixtures####
@pytest.fixture
def game() -> Go:
    """
    Returns a 19x19 Go game with two players
    """
    return Go(19, 2)

@pytest.fixture
def game_3() -> Go:
    """
    Returns a 19x19 Go game with three players
    """
    return Go(19, 3)

##################
#Helper Functions#
##################
def load_board_with_pieces(n: int) -> Go:
    """
    loads a n x n board with two players and sets some pieces on the sides of
    the board

    Inputs:
        n [int]: the size of the board
        superko [bool]: superko rule status

    Returns Go: loaded game with some moves played
    """
    pieces_positions = [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1), (n//2, 0),
                        (0, n//2), (n-1, n//2), (n//2, n-1)]

    initial_grid: list[list[Union[int, None]]] = [[None for _ in range(n)]
                                               for _ in range(n)]

    for p, pos in enumerate(pieces_positions):
        i, j = pos
        if p % 2 == 0:
            initial_grid[i][j] = 1
        else:
            initial_grid[i][j] = 2

    game = Go(n, 2)
    game.load_game(1, initial_grid)

    return game


def sets_grid(game: Go, lst: list[tuple[int, int]]) -> Go:
    """
    Loads a 19x19 2-player Go game with values at positions in the list
    provided. Follows the order/turn while setting the pieces

    Input:
        lst [lst[tuple]]: list of positions to be occupied with pieces

    Returns: Go game set with pieces at the locations given
    """
    initial_grid: list[list[Union[int, None]]] = [[None for _ in range(19)]
                                                  for _ in range(19)]

    for p, pos in enumerate(lst):
        i, j = pos
        if p % 2 == 0:
            initial_grid[i][j] = 1
        else:
            initial_grid[i][j] = 2

    if len(lst) % 2 == 0:
        game.load_game(1, initial_grid)
    else:
        game.load_game(2, initial_grid)

    return game

def sets_grid_no_order(white: list[tuple[int, int]], black:
                       list[tuple[int, int]], super_ko: bool = False) -> Go:
    """
    Loads a 19x19 2-player Go game with values at positions in the lists
    provided. Does not follow the order/turn in setting the pieces

    Input:
        white [lst[tuple]]: list of positions to be occupied with white pieces
        black [lst[tuple]]: list of positions to be occupied with black pieces
        super_ko [bool]: Status of the superko rule

    Returns: Go game set with pieces at the locations given
    """
    initial_grid: list[list[Union[int, None]]] = [[None for _ in range(19)]
                                                  for _ in range(19)]
    for pos in white:
        i, j = pos
        initial_grid[i][j] = 1

    for pos in black:
        i, j = pos
        initial_grid[i][j] = 2

    if super_ko:
        game = Go(19, 2, True)
    else:
        game = Go(19, 2)

    game.load_game(1, initial_grid)

    return game

########
##Tests#
########
@pytest.mark.parametrize("size", [i for i in range(4, 20)])
def test_board_1(size: int) -> None:
    """
    Tests the construction of a Go game. Constructs boards of different sizes
    and verify that they were constructed correctly. Assume just two players.
    """
    game = Go(size, 2)

    assert game.grid == [[None] * size for _ in range(size)]
    assert game.num_players == 2
    assert game.turn == 1


def test_size_1(game: Go) -> None:
    """
    Tests the size of the 19 x 19 board
    """
    assert len(game.grid) == 19
    assert all(len(row) == 19 for row in game.grid)


@pytest.mark.parametrize("players", [n for n in range(2, 9)])
def test_players_1(players: int) -> None:
    """
    Test the number of players in the game in a 19 x 19 board
    """
    game = Go(19, players)
    assert game.num_players == players


def test_turn_1(game: Go) -> None:
    """
    Tests the turn property in a 19 x 19 board
    """
    assert game.turn == 1
    game.apply_move((0, 1))
    assert game.turn == 2
    game.apply_move((1, 0))
    assert game.turn == 1
    game.pass_turn()
    assert game.turn == 2


@pytest.mark.parametrize("n", [19, 9, 13])
def test_piece_legal_1(n: int) -> None:
    """
    Constructs a 9x9, 13x13 and 19x19 Go game and test the piece_at and
    legal move
    """
    game = load_board_with_pieces(n)

    for i in range(n):
        for j in range(n):
            pos = (i, j)
            legal = game.legal_move(pos)
            piece = game.piece_at(pos)
            if (i, j) in [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1), (n//2, 0),
                        (0, n//2), (n-1, n//2), (n//2, n-1)]:
                assert piece is not None
                assert not legal
            else:
                assert piece is None
                assert legal

    with pytest.raises(ValueError):
        game.legal_move((-1, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, -1))

    with pytest.raises(ValueError):
        game.legal_move((n, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, n))


@pytest.mark.parametrize("n", [19, 9, 13])
def test_available_moves_1(n: int) -> None:
    """
    constructs a 19x19, 9x9 and 13x13 Go game and test the available_moves
    """
    game = load_board_with_pieces(n)
    expected_moves = []
    for i in range(game.size):
        for j in range(game.size):
            if not (i, j) in [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1), (n//2, 0),
                        (0, n//2), (n-1, n//2), (n//2, n-1)]:
                expected_moves.append((i, j))

    assert game.available_moves == expected_moves


def test_apply_move_1(game: Go) -> None:
    """
    Constructs a 19x19 Go game, calls apply_move on a legal position,
    and verifies that turn and piece_at return the correct values.
    """
    assert game.turn == 1

    legal_position = (3, 5)
    game.apply_move(legal_position)

    assert game.turn == 2
    assert game.piece_at(legal_position) == 1
    assert all(game.piece_at((i, j)) is None for i in range(19) for j in
               range(19) if (i, j) != legal_position)


def test_progress_1(game: Go) -> None:
    """
    Verifies that done and outcome return values consistent with a game
    in progress in a 19 X 19 board
    """
    assert game.turn == 1
    game.apply_move((3, 5))
    assert game.piece_at((3, 5)) == 1

    assert game.turn == 2
    game.apply_move((4, 6))
    assert game.piece_at((4, 6)) == 2

    assert not game.done
    assert game.outcome == []


def test_end_1(game: Go) -> None:
    """
    Tests apply_move a few times in a way that won't result in any captures.
    Then, makes both players pass to make the game end. (19 X 19 board)
    """
    game.apply_move((0, 1))
    game.apply_move((10, 1))
    game.apply_move((12, 3))

    game.pass_turn()
    game.pass_turn()

    assert game.done
    assert game.outcome == [1]


@pytest.mark.parametrize("size", [9, 13])
def test_board_2(size: int) -> None:
    """
    Constructs a 9x9 and a 13x13 game and test the size, num_players, and turn
    """
    game = Go(size, 2)

    assert len(game.grid) == size
    assert all(len(row) == size for row in game.grid)
    assert game.num_players == 2
    assert game.turn == 1


def test_legal_2(game: Go) -> None:
    """
    constructs a 19x19 Go game and verifies that legal_move and available_moves
    allow moves in any position of the board.
    """
    expected_moves = []
    for i in range(19):
        for j in range(19):
            assert game.legal_move((i, j))
            expected_moves.append((i, j))

    assert game.available_moves == expected_moves


def test_moves_19(game: Go) -> None:
    """
    Makes two moves and verifies that the pieces were placed on the board, and
    that the turn has been updated correctly after each move.
    """
    game.apply_move((3, 2))
    assert game.piece_at((3,2)) == 1
    assert game.turn == 2
    game.apply_move((7, 3))
    assert game.piece_at((7, 3)) == 2
    assert game.turn == 1


def test_legal_3(game: Go) -> None:
    """
    Makes a move, and verifies that the position of that move is no longer a
    legal move.
    """
    game.apply_move((5, 5))
    assert not game.legal_move((5, 5))


def test_pass_2(game: Go) -> None:
    """
    Makes a move, then passes. Verifies that the turn is updated correctly.
    """
    game.apply_move((9, 6))
    game.pass_turn()
    assert game.turn == 1


def test_pass_3(game: Go) -> None:
    """
    Makes a move, then passes twice. Verifies that the game ends.
    """
    game.apply_move((8, 4))
    game.pass_turn()
    game.pass_turn()
    assert game.done


def test_capture_1(game: Go) -> None:
    """
    Loads moves that will result in one piece being captured. Verifies that the
    piece is indeed captured.
    """
    moves = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5), (6, 6), (10, 6)]

    game = sets_grid(game, moves)

    game.apply_move((5, 7))

    assert game.piece_at((5, 6)) == None


def test_capture_2(game: Go) -> None:
    """
    Loads moves that will result in multiple pieces being captured. Verifies
    that all the pieces were indeed captured.
    """
    moves = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5), (6, 6), (10, 6), (6, 7),
             (5, 7), (5, 8), (10, 7)]

    game = sets_grid(game, moves)

    game.apply_move((4, 7))

    assert game.piece_at((5, 6)) == None
    assert game.piece_at((5, 7)) == None


def test_ko_1(game: Go) -> None:
    """
    Makes moves in such a way that there will end up being a move that would
    violate the ko rule. Checks that legal_move identifies the move as illegal.
    """
    moves= [(5, 6), (5, 5), (4, 7), (4, 6), (6, 7), (6, 6), (5, 8)]

    game = sets_grid(game, moves)

    game.apply_move((5, 7))

    assert not game.legal_move((5, 6))


def test_superko_1() -> None:
    """
    Makes moves in such a way that there will end up being a move that would
    violate the super ko rule. Checks that legal_move identifies the move as
    illegal.
    """
    white_moves = [(9, 5), (9, 6), (9, 7), (9, 8), (8, 8), (7, 8), (7, 9),
                   (6, 9), (5, 9), (7, 5), (6, 5), (5, 6)]
    black_moves = [(8, 5), (8, 6), (8, 7), (7, 7), (6, 7), (6, 8), (5, 8),
                   (6, 6)]

    game: Go = sets_grid_no_order(white_moves, black_moves, True)

    game.apply_move((5, 7))
    game.apply_move((5, 5))

    assert not game.legal_move((5, 6))


def test_scores_1() -> None:
    """
    Makes several moves that don't result in any territories being created, and
    verifies that scores returns the correct values.
    """
    game: Go = load_board_with_pieces(19)

    assert game.scores() == {1: 4, 2: 4}


def test_scores_2(game: Go) -> None:
    """
    Makes several moves that will result in one territory being created, and
    verifies that scores returns the correct values.
    """
    moves = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5), (6, 6), (10, 6)]

    game = sets_grid(game, moves)

    game.apply_move((5, 7))

    assert game.scores() == {1: 3, 2: 5}


def test_outcome_4(game: Go) -> None:
    """
    Makes several moves that will result in one territory being created. Ends
    the game and, verifies the outcome.
    """
    moves = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5), (6, 6), (10, 6)]

    game = sets_grid(game, moves)

    game.apply_move((5, 7))

    game.pass_turn()
    game.pass_turn()

    assert game.outcome == [2]


def test_moves_4(game_3: Go) -> None:
    """
    Makes three moves, and verifies that the pieces were placed on the board,
    and that the turn has been updated correctly after each move.
    """
    game_3.apply_move((0, 3))
    assert game_3.piece_at((0, 3)) == 1
    assert game_3.turn == 2
    game_3.apply_move((10, 11))
    assert game_3.piece_at((10, 11)) == 2
    assert game_3.turn == 3
    game_3.apply_move((5, 9))
    assert game_3.piece_at((5, 9)) == 3
    assert game_3.turn == 1


def test_end_4(game_3: Go) -> None:
    """
    Makes a move, then passes three times. Verifies that the game ends.
    """
    game_3.apply_move((0, 1))
    game_3.pass_turn()
    game_3.pass_turn()
    game_3.pass_turn()

    assert game_3.done


def test_simulate_move_1(game: Go) -> None:
    """
    Test that simulating a move creates a new game
    """
    new_go = game.simulate_move((5, 5))

    # Check that the original Go object has not been modified
    assert game.piece_at((5, 5)) is None
    assert game.turn == 1

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 5)) == 1
    assert new_go.turn == 2


def test_simulate_move_2(game: Go) -> None:
    """
    After making a few moves, check that simulating a move
    correctly creates a new game.
    """
    initial_moves = [(3, 3), (6, 16), (1, 1), (13, 0), (16, 1), (18, 15),
                     (13, 14), (2, 10), (1, 17), (3, 13), (11, 2), (2, 8),
                     (13, 11), (11, 0), (4, 17), (3, 6), (16, 2), (5, 2),
                     (14, 8), (13, 2)]

    game = sets_grid(game, initial_moves)

    new_go = game.simulate_move((5, 5))

    # Check that the original GoFake object has not been modified
    assert game.piece_at((5, 5)) is None
    for move in initial_moves:
        assert game.piece_at(move) is not None
    assert game.turn == 1

    # Check that the move was applied in the new GoFake object
    assert new_go.piece_at((5, 5)) == 1
    for move in initial_moves:
        assert new_go.piece_at(move) is not None
    assert new_go.turn == 2


def test_simulate_move_3(game: Go) -> None:
    """
    We place one piece in position (5, 6) and then
    simulate placing a piece in position (5, 7).
    The piece in position (5, 6) should be captured
    (but only in the new game created by simulate_move)
    """
    game.apply_move((5, 6))
    assert game.piece_at((5, 6)) == 1

    new_go = game.simulate_move((5, 7))

    # Check that the original Go object has not been modified
    assert game.piece_at((5, 6)) == 1
    assert game.piece_at((5, 7)) is None
    assert game.turn == 2

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 6)) == 1
    assert new_go.piece_at((5, 7)) == 2
    assert new_go.turn == 1


def test_simulate_move_4(game: Go) -> None:
    """
    Check that simulating a pass works correctly.
    """
    new_go = game.simulate_move(None)

    # Check that the original Go object has not been modified
    assert game.turn == 1

    # Check that the pass was applied in the new Go object
    assert new_go.turn == 2


def test_simulate_move_5(game: Go) -> None:
    """
    Check that simulating two consecutive passes works correctly.
    """
    new_go = game.simulate_move(None).simulate_move(None)

    # Check that the original Go object has not been modified
    assert game.turn == 1
    assert not game.done

    # Check that the passes were applied in the new Go object
    assert new_go.done


def test_grid_1(game: Go) -> None:
    """
    Check that grid for an empty game is exported correctly
    """
    grid = game.grid

    for row in range(game.size):
        for col in range(game.size):
            assert grid[row][col] is None


def test_grid_2(game: Go) -> None:
    """
    Check that grid returns a deep copy of the board's grid,
    and that modifying grid's return value doesn't modify
    the game's board
    """
    grid = game.grid

    grid[5][5] = 1

    assert game.piece_at((5, 5)) is None, (
        "grid() returned a shallow copy of the game's board. "
        "Modifying the return value of grid() should not "
        "affect the game's board."
    )


def test_grid_3(game: Go) -> None:
    """
    Check that grid returns a correct copy of the board after making
    a few moves (none of the moves will result in a capture)
    """
    moves = [(3, 3), (6, 16), (1, 1), (13, 0), (16, 1), (18, 15), (13, 14),
             (2, 10), (1, 17), (3, 13), (11, 2), (2, 8), (13, 11), (11, 0),
             (4, 17), (3, 6), (16, 2), (5, 2), (14, 8), (12, 2)]

    game = sets_grid(game, moves)

    grid = game.grid

    for row in range(game.size):
        for col in range(game.size):
            assert grid[row][col] == game.piece_at((row, col))

def test_ten_capture() -> None:
    """
    Loads game and tests the capture of 10 pieces
    """
    white_moves = [(8, 7), (9, 7), (10, 7), (11, 8), (11, 10), (10, 11), (9, 11)
                   , (8, 11), (7, 10), (7, 9), (7, 8)]
    black_moves = [(8, 8), (8, 9), (8, 10), (9, 8), (9, 9), (9, 10), (10, 8),
                   (10, 9), (10, 10), (11, 9), (17, 17)]

    game = sets_grid_no_order(white_moves, black_moves)
    game.apply_move((12, 9))

    assert game.scores() == {1: 22, 2: 1}

def test_scores_6() -> None:
    """
    Loads two-player game that ends withone  territory per player, and one
    neutral territory. The test must validate that the scores for each player
    are as expected
    """
    white_moves = [(7, 6), (6, 7), (7, 8), (8, 7), (10, 8), (12, 8)]
    black_moves = [(6, 10), (7, 9), (8, 10), (7, 11), (11, 7), (11, 9)]

    game = sets_grid_no_order(white_moves, black_moves)

    game.pass_turn()
    game.pass_turn()

    assert game.scores() == {1: 7, 2: 7}

def test_scores_7(game_3: Go) -> None:
    """
    Loads 3-player game that ends with one territory per player, and one
    neutral territory. The test must validate that the scores for each player
    are as expected
    """
    white_moves = [(7, 5), (6, 6), (7, 7), (8, 6), (10, 9), (11, 10)]
    black_moves = [(7, 8), (6, 9), (7, 10), (8, 9), (11, 8)]
    red_moves = [(7, 11), (6, 12), (7, 13), (8, 12), (12, 9)]

    initial_grid = [[None for _ in range(19)] for _ in range(19)]

    for pos in white_moves:
        i, j = pos
        initial_grid[i][j] = 1

    for pos in black_moves:
        i, j = pos
        initial_grid[i][j] = 2

    for pos in red_moves:
        i, j = pos
        initial_grid[i][j] = 3

    game_3.load_game(1, initial_grid)
    game_3.pass_turn()
    game_3.pass_turn()
    game_3.pass_turn()

    assert game_3.scores() == {1: 7, 2: 6, 3: 6}

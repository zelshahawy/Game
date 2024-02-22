"""
Tests for Go
"""
import pytest
from go import Go


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
def create_board_with_pieces(n: int, players: int, superko: bool = False) -> Go:
    """
    Creates a board n x n and plays some moves in it

    Inputs:
        n [int]: the size of the board
        players [int]: number of players
        superko [bool]: superko rule status

    Returns Go: The game with some moves playes
    """
    game = Go(n, players, superko)
    pieces_positions = [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1), (n//2, 0),
                        (0, n//2), (n-1, n//2), (n//2, n-1)]

    for pos in pieces_positions:
        game.apply_move(pos)

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
    game = create_board_with_pieces(n, 2)

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
    game = Go(n, 2)
    expected_moves: list[tuple[int, int]] = []
    for i in range(game.size):
        for j in range(game.size):
            expected_moves.append((i, j))

    assert game.available_moves == expected_moves

    for i in range(4):
        for j in range(4):
            game.apply_move((i, j))
            expected_moves.remove((i, j))

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
    for i in range(19):
        for j in range(19):
            assert game.legal_move((i, j))
            assert (i, j) in game.available_moves


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
    Makes moves that will result in one piece being captured. Verifies that the
    piece is indeed captured.
    """
    moves: list[tuple[int, int]] = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5),
                                    (6, 6), (10, 6), (5, 7)]

    for move in moves:
        game.apply_move(move)

    assert game.piece_at((5, 6)) == None


def test_capture_2(game: Go) -> None:
    """
    Makes moves that will result in multiple pieces being captured. Verifies
    that all the pieces were indeed captured.
    """
    moves: list[tuple[int, int]] = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5),
                                    (6, 6), (10, 6), (6, 7), (5, 7), (5, 8),
                                    (10, 7), (4, 7)]

    for move in moves:
        game.apply_move(move)

    assert game.piece_at((5, 6)) == None
    assert game.piece_at((5, 7)) == None


def test_ko_1(game: Go) -> None:
    """
    Makes moves in such a way that there will end up being a move that would
    violate the ko rule. Checks that legal_move identifies the move as illegal.
    """
    moves: list[tuple[int, int]] = [(5, 6), (5, 5), (4, 7), (4, 6), (6, 7),
                                    (6, 6), (5, 8), (5, 7)]

    for move in moves:
        game.apply_move(move)

    assert not game.legal_move((5, 6))


def test_superko_1() -> None:
    """
    Makes moves in such a way that there will end up being a move that would
    violate the super ko rule. Checks that legal_move identifies the move as
    illegal.
    """
    game: Go = Go(19, 2, True)
    moves: list[tuple[int, int]] = [(5, 6), (5, 5), (4, 7), (4, 6), (6, 7),
                                    (6, 6), (5, 8), (5, 7), (10, 5), (10, 9)]

    for move in moves:
        game.apply_move(move)

    assert not game.legal_move((5, 6))


def test_scores_1() -> None:
    """
    Makes several moves that don't result in any territories being created, and
    verifies that scores returns the correct values.
    """
    game: Go = create_board_with_pieces(19, 2)

    assert game.scores() == {1: 4, 2: 4}


def test_scores_2(game: Go) -> None:
    """
    Makes several moves that will result in one territory being created, and
    verifies that scores returns the correct values.
    """
    moves: list[tuple[int, int]] = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5),
                                    (6, 6), (10, 6), (5, 7)]

    for move in moves:
        game.apply_move(move)

    assert game.scores() == {1: 3, 2: 5}


def test_outcome_4(game: Go) -> None:
    """
    Makes several moves that will result in one territory being created. Ends
    the game and, verifies the outcome.
    """
    moves: list[tuple[int, int]] = [(5, 6), (4, 6), (10, 4), (5, 5), (10, 5),
                                    (6, 6), (10, 6), (5, 7)]

    for move in moves:
        game.apply_move(move)

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
    initial_moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 0),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 0),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (13, 2),
    ]

    for move in initial_moves:
        game.apply_move(move)

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
    assert new_go.piece_at((5, 6)) is None
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
    moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 0),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 0),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (12, 2),
    ]

    for move in moves:
        game.apply_move(move)

    grid = game.grid

    for row in range(game.size):
        for col in range(game.size):
            assert grid[row][col] == game.piece_at((row, col))

"""
Tests for Go
"""
import pytest
from go import Go


####Fixtures####
@pytest.fixture
def game() -> Go:
    """
    Returns a 19 x 19 Go game with two players
    """
    return Go(19, 2)

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
@pytest.mark.parametrize("side", [i for i in range(4, 20)])
def test_board_construction_1(side: int) -> None:
    """
    Tests the construction of a Go game. Constructs boards of different sizes
    and verify that they were constructed correctly. Assume just two players.
    """
    game = Go(side, players = 2, superko = False)

    assert game.grid == [[None] * side for _ in range(side)]
    assert game.num_players == 2
    assert game.turn == 1

def test_board_size_1(game: Go) -> None:
    """
    Tests the size of the 19 x 19 board
    """
    assert len(game.grid) == 19
    assert all(len(row) == 19 for row in game.grid)

@pytest.mark.parametrize("players", [n for n in range(2, 9)])
def test_num_players_1(players: int) -> None:
    """
    Test the number of players in the game in a 19 x 19 board
    """
    game = Go(19, players)
    assert game.num_players == players

def test_turn_property_1(game: Go) -> None:
    """
    Tests the turn property in a 19 x 19 board
    """
    assert game.turn == 1
    game.apply_move((0, 1))
    assert game.turn == 2
    game.apply_move((1, 0))
    assert game.turn == 3
    game.pass_turn()
    assert game.turn == 4

@pytest.mark.parametrize("n", [19, 9, 13])
def test_piece_legal_2(n: Go) -> None:
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
def test_available_moves_2(n: int) -> None:
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

def test_game_in_progress_1(game: Go) -> None:
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

def test_apply_move_end_1(game: Go) -> None:
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
def test_construction_properties_2(size: int) -> None:
    """
    Constructs a 9x9 and a 13x13 game and test the size, num_players, and turn
    """
    game = create_board_with_pieces(size, 3)

    assert len(game.grid) == size
    assert all(len(row) == size for row in game.grid)
    assert game.num_players == 3
    assert game.turn == 3

###the following tests will consits of 19x19 board in different scenarios
def test_legal_available_19(game: Go) -> None:
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

def test_legal_19(game: Go) -> None:
    """
    Makes a move, and verifies that the position of that move is no longer a
    legal move.
    """
    game.apply_move((5, 5))
    assert not game.legal_move((5, 5))

def test_pass_19(game: Go) -> None:
    """
    Makes a move, then passes. Verifies that the turn is updated correctly.
    """
    game.apply_move((9, 6))
    game.pass_turn()
    assert game.turn == 1

def test_pass_twice_19(game: Go) -> None:
    """
    Makes a move, then passes twice. Verifies that the game ends.
    """
    game.apply_move((8, 4))
    game.pass_turn()
    game.pass_turn()
    assert game.done

def test_capture_19(game: Go) -> None:
    """
    Makes moves that will result in one piece being captured. Verifies that the
    piece is indeed captured.
    """

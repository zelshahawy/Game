"""
Tests for Go
"""
import pytest
from go import Go


###Fixtures
@pytest.fixture
def game() -> Go:
    return Go(19, 2)                                                #how do i use this in code?


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


###################
#Tests Milestone 1#
###################

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

def test_board_size_1() -> None:
    """
    Tests the size of the 19 x 19 board
    """
    game = create_board_with_pieces(19, players=2)

    assert len(game.grid) == 19
    assert all(len(row) == 19 for row in game.grid)

@pytest.mark.parametrize("players", [n for n in range(2, 9)])
def test_num_players_1(players: int) -> None:
    """
    Test the number of players in the game in a 19 x 19 board
    """
    game = create_board_with_pieces(19, players)
    assert game.num_players == players

def test_turn_property_1() -> None:
    """
    Tests the turn property in a 19 x 19 board
    """
    game = create_board_with_pieces(19, 4)

    assert game.turn == 1
    game.apply_move((0, 1))
    assert game.turn == 2
    game.apply_move((1, 0))
    assert game.turn == 3
    game.pass_turn()
    assert game.turn == 4

def test_piece_at_1() -> None:
    """
    Test piece_at method in a 19 x 19 board
    """
    game = create_board_with_pieces(19, 4)

    for i in range(19):
        for j in range(19):
            piece = game.piece_at((i, j))
            if (i, j) in [(0, 0), (0, 18), (18, 0), (18, 18), (9, 0), (0, 9),
                          (18, 9), (9, 18)]:
                assert piece is not None
            else:
                assert piece is None

def test_legal_move_1() -> None:
    """
    Tests legal_move method in a 19 x 19 board
    """
    game = create_board_with_pieces(19, 2)

    for i in range(19):
        for j in range(19):
            pos = (i, j)
            legal = game.legal_move(pos)
            if pos in [(0, 0), (0, 18), (18, 0), (18, 18), (9, 0), (0, 9),
                       (18, 9), (9, 18)]:
                assert not legal
            else:
                assert legal

    with pytest.raises(ValueError):
        game.legal_move((-1, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, -1))

    with pytest.raises(ValueError):
        game.legal_move((19, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, 19))


def test_available_moves_1() -> None:
    """
    Checks available_moves when the game is started and when moves are made in a
    19 x 19 board
    """
    game = Go(19, 4)

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

def test_apply_move_1() -> None:
    """
    Constructs a 19x19 Go game, calls apply_move on a legal position,
    and verifies that turn and piece_at return the correct values.
    """
    game = Go(19, 2)

    assert game.turn == 1

    legal_position = (3, 5)
    game.apply_move(legal_position)

    assert game.turn == 2
    assert game.piece_at(legal_position) == 1
    assert all(game.piece_at((i, j)) is None for i in range(19) for j in
               range(19) if (i, j) != legal_position)


def test_game_in_progress_1() -> None:
    """
    Verifies that done and outcome return values consistent with a game
    in progress in a 19 X 19 board
    """
    game = Go(19, 2)

    assert game.turn == 1
    game.apply_move((3, 5))
    assert game.piece_at((3, 5)) == 1

    assert game.turn == 2
    game.apply_move((4, 6))
    assert game.piece_at((4, 6)) == 2

    assert not game.done
    assert game.outcome == []


def test_apply_move_end_1() -> None:
    """
    Tests apply_move a few times in a way that won't result in any captures.
    Then, makes both players pass to make the game end. (19 X 19 board)
    """
    game = Go(19, 2)

    game.apply_move((0, 1))
    game.apply_move((10, 1))
    game.apply_move((12, 3))

    game.pass_turn()
    game.pass_turn()

    assert game.done
    assert game.outcome == [1]


###################
#Tests Milestone 2#
###################

def test_construction_properties_2() -> None:
    """
    Constructs a 9x9 Go game and test the size, num_players, and turn properties.
    """
    game = create_board_with_pieces(9, 3)

    assert len(game.grid) == 9
    assert all(len(row) == 9 for row in game.grid)
    assert game.num_players == 3
    assert game.turn == 3

def test_piece_at_9x9() -> None:
    """
    constructs a 9x9 Go game and test the piece_at
    """
    game = create_board_with_pieces(9, 2)

    for i in range(9):
        for j in range(9):
            piece = game.piece_at((i, j))                                   #kinda repeated code. can i use helper tests?
            if (i, j) in [(0, 0), (0, 8), (8, 0), (8, 8), (4, 0), (0, 4),
                          (8, 4), (4, 8)]:
                assert piece is not None
            else:
                assert piece is None

def test_legal_move_9x9() -> None:
    """
    constructs a 9x9 Go game and test the legal_move
    """
    game = create_board_with_pieces(9, 2)

    for i in range(9):
        for j in range(9):
            pos = (i, j)
            legal = game.legal_move(pos)
            if pos in [(0, 0), (0, 8), (8, 0), (8, 8), (4, 0), (0, 4),
                       (8, 4), (4, 8)]:
                assert not legal
            else:
                assert legal                                                #very repeated code. i just have to learn how to use a test helper

    with pytest.raises(ValueError):
        game.legal_move((-1, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, -1))

    with pytest.raises(ValueError):
        game.legal_move((9, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, 9))


def test_available_moves_9x9() -> None:
    """
    constructs a 9x9 Go game and test the legal_move
    """
    game = Go(9, 2)

    expected_moves: list[tuple[int, int]] = []
    for i in range(game.size):
        for j in range(game.size):
            expected_moves.append((i, j))                                 #helper function needed

    assert game.available_moves == expected_moves

    for i in range(4):
        for j in range(4):
            game.apply_move((i, j))
            expected_moves.remove((i, j))

    assert game.available_moves == expected_moves


############room for so many helpers. 13X13####################################
def test_construction_properties_13x13() -> None:
    """
    Constructs a 13x13 Go game and test the size, num_players, and turn
    properties.
    """
    game = create_board_with_pieces(13, 3)

    assert len(game.grid) == 13                                                  #parametarize
    assert all(len(row) == 13 for row in game.grid)
    assert game.num_players == 3
    assert game.turn == 3

def test_piece_at_13x13() -> None:
    """
    constructs a 13x13 Go game and test the piece_at
    """
    game = create_board_with_pieces(13, 2)

    for i in range(13):
        for j in range(13):
            piece = game.piece_at((i, j))                                      #kinda repeated code. can i use helper tests?
            if (i, j) in [(0, 0), (0, 12), (12, 0), (12, 12), (6, 0), (0, 6),
                          (12, 6), (6, 12)]:
                assert piece is not None
            else:
                assert piece is None

def test_legal_move_13x13() -> None:
    """
    constructs a 13x13 Go game and test the legal_move
    """
    game = create_board_with_pieces(13, 2)

    for i in range(13):
        for j in range(13):
            pos = (i, j)
            legal = game.legal_move(pos)
            if pos in [(0, 0), (0, 12), (12, 0), (12, 12), (6, 0), (0, 6),
                        (12, 6), (6, 12)]:
                assert not legal
            else:
                assert legal                                                #very repeated code. i just have to learn how to use a test helper

    with pytest.raises(ValueError):
        game.legal_move((-1, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, -1))

    with pytest.raises(ValueError):
        game.legal_move((13, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, 13))


def test_available_moves_13x13() -> None:
    """
    constructs a 9x9 Go game and test the legal_move
    """
    game = Go(13, 2)

    expected_moves: list[tuple[int, int]] = []
    for i in range(game.size):
        for j in range(game.size):
            expected_moves.append((i, j))                                 #helper function needed

    assert game.available_moves == expected_moves

    for i in range(4):
        for j in range(4):
            game.apply_move((i, j))
            expected_moves.remove((i, j))

    assert game.available_moves == expected_moves

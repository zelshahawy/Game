"""
Tests for Milestone 1
"""
import pytest
from go import Go


def create_board_with_pieces(n: int, players: int, superko: bool = False) -> Go:
    """
    Creates a board s x s and plays some moves in it

    Inputs:
        n [int]: the size of the board
        players [int]: number of players
        superko [bool]: superko rule status

    Returns Go: The game witb some moves playes
    """
    game = Go(n, players, superko)
    pieces_positions = [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1), (n//2, 0),
                        (0, n//2), (n-1, n//2), (n//2, n-1)]

    for pos in pieces_positions:
        game.apply_move(pos)

    return game

@pytest.mark.parametrize("side", [i for i in range(4, 20)])
def test_board_construction(side: int) -> None:
    """
    Tests the construction of a Go game. Constructs boards of different sizes
    and verify that they were constructed correctly. Assume just two players.
    """
    game = Go(side, players = 2, superko = False)

    assert game.grid == [[None] * side for _ in range(side)]
    assert game.num_players == 2
    assert game.turn == 1

def test_board_size() -> None:
    """
    Tests the size of the board
    """
    game = create_board_with_pieces(19, players=2)

    assert len(game.grid) == 19
    assert all(len(row) == 19 for row in game.grid)

@pytest.mark.parametrize("players", [n for n in range(2, 9)])
def test_num_players(players: int) -> None:
    """
    Test the number of players in the game
    """
    game = create_board_with_pieces(19, players)
    assert game.num_players == players

def test_turn_property() -> None:
    """
    Tests the turn property
    """
    game = create_board_with_pieces(19, 4)

    assert game.turn == 1
    game.apply_move((0, 1))
    assert game.turn == 2
    game.apply_move((1, 0))
    assert game.turn == 3
    game.pass_turn()
    assert game.turn == 4

def test_piece_at() -> None:
    """
    Test piece_at method
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

def test_legal_move() -> None:
    """
    Tests legal_move method
    """
    game = create_board_with_pieces(19, 2)

    for i in range(19):
        for j in range(19):
            pos = (i, j)
            legal = game.legal_move(pos)
            if pos in [(0, 0), (0, 18), (18, 0), (18, 18), (9, 0), (0, 9),
                       (18, 9), (9, 18)]:
                assert not legal
            elif 0 <= i < 19 and 0 <= j < 19:
                assert legal

    with pytest.raises(ValueError):
        game.legal_move((-1, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, -1))

    with pytest.raises(ValueError):
        game.legal_move((19, 0))

    with pytest.raises(ValueError):
        game.legal_move((0, 19))


def test_available_moves() -> None:
    """
    Checks available_moves when the game is started and when moves are made.

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

def test_apply_move() -> None:
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


def test_game_in_progress() -> None:
    """
    Verifies that done and outcome return values consistent with a game
    in progress.
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


def test_apply_move_end() -> None:
    """
    Tests apply_move a few times in a way that won't result in any captures.
    Then, makes both players pass to make the game end.
    """
    game = Go(19, 2)

    game.apply_move((0, 1))
    game.apply_move((10, 1))
    game.apply_move((20, 16))

    game.pass_turn()
    game.pass_turn()

    assert game.done
    assert game.outcome == [1]

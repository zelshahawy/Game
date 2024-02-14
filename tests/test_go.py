"""
Tests for Milestone 2
"""
import pytest
from go import *


@pytest.mark.parametrize("side", [i for i in range(4, 20)])
def test_board_construction(side) -> None:
    """
    Tests the construction of a Go game. Constructs boards of different sizes
    and verify that they were constructed correctly. Assume just two players.
    """
    game = Go(side, players = 2, superko = False)

    assert game.grid == [[None] * side for _ in range(side)]
    assert game.num_players == 2
    assert game.turn == 1

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

def test_board_size() -> None:
    """
    Tests the size of the board
    """
    game = create_board_with_pieces(19, players=2)

    assert len(game.grid) == 19
    assert all(len(row) == 19 for row in game.grid)

@pytest.mark.parametrize("players", [n for n in range(2, 9)])
def test_num_players(players) -> None:
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
    assert game.pass_turn()
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

                                                                                    #do not forget the exceptions
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
        game.legal_move((-2, 0))
        game.legal_move((0, -2))
        game.legal_move((19, 0))
        game.legal_move((0, 19))

def test_legal_move_superko() -> None:
    """
    Tests legal_move method with the superko rule
    """
    game = create_board_with_pieces(19, 2, True)

    game.apply_move((3, 5))
    game.apply_move((3, 4))
    game.apply_move((2, 6))
    game.apply_move((2, 5))
    game.apply_move((3, 7))
    game.apply_move((13, 15))
    game.apply_move((4, 6))
    game.apply_move((4, 5))
    game.apply_move((7, 8))
    game.apply_move((3, 6))

    assert not game.legal_move((3, 5))
    assert (3, 5) not in game.available_moves

def test_self_capture() -> None:
    """
    Test that it is an illegal move when a piece captures itself. Tests the
    available_move method
    """
    game = create_board_with_pieces(19, 2)

    game.apply_move((3, 5))
    game.apply_move((3, 4))
    game.apply_move((2, 6))
    game.apply_move((2, 5))
    game.apply_move((3, 7))
    game.apply_move((13, 15))
    game.apply_move((4, 6))

    assert not game.legal_move((3, 6))
    assert (3, 6) not in game.available_moves

def test_available_moves_2() -> None:
    """
    Checks available_moves when the game is started and when moves are made
    """
    game = Go(19, 4)

    expected_moves: list[tuple[int, int]] = []
    for i in range(game.size):
        for j in range(game.size):
            expected_moves.append((i, j))

    assert game.available_moves == expected_moves

    game.apply_move((3, 5))
    expected_moves[3].pop(5)
    game.apply_move((3, 4))
    expected_moves[3].pop(4)
    game.apply_move((2, 6))
    expected_moves[2].pop(6)
    game.apply_move((2, 5))
    expected_moves[2].pop(5)                                                 #add all this code to helper
    game.apply_move((3, 7))
    expected_moves[3].pop(7)
    game.apply_move((13, 15))
    expected_moves[13].pop(15)
    game.apply_move((4, 6))
    expected_moves[4].pop(6)

    expected_moves[3].pop(6)

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

    game.apply_move((3, 5))
    game.apply_move((4, 6))
    game.apply_move((5, 7))

    assert not game.done
    assert game.outcome == []

    game.pass_turn()
    game.pass_turn()

    assert game.done
    assert game.outcome == [1, 2]

def test_methods_2() -> None:
    """
    Construct a 19x19 Go game, call apply_move on a legal position, and verify
    that turn and piece_at return the correct values. Verify that done and
    outcome return values consistent with a game in progress.
    """
    return NotImplementedError

def test_methods_3() -> None:
    """
    Construct a 19x19 Go game, call apply_move a few times in a way that won't
    result in any captures. Then, make both players pass to make the game end.
    Verify that the grid contains the expected pieces, and that done and outcome
    return values consistent with a game that has ended.
    """
    return NotImplementedError
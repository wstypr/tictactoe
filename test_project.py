from project import *
from pytest import raises

def test_get_board_size():
    min_size = 1
    max_size = 10
    assert get_board_size(min_size, max_size, "1") == 1
    assert get_board_size(min_size, max_size, "10") == 10

def test_get_board_size_error1():
    min_size = 1
    max_size = 10
    with raises(ValueError):
        get_board_size(min_size, max_size, "0")

def test_get_board_size_error2():
    min_size = 1
    max_size = 10
    with raises(ValueError):
        get_board_size(min_size, max_size, "11")

def test_get_board_size_error3():
    min_size = 1
    max_size = 10
    with raises(ValueError):
        get_board_size(min_size, max_size, "ad")


def test_get_game_mode():
    assert get_game_mode("3") == 3
    with raises(ValueError):
        get_game_mode("4")


def test_get_move():
    available_move = ["11", "22", "33"]
    assert get_move(available_move, "11")
    assert available_move == ["22", "33"]

def test_get_move_error():
    available_move = ["11", "22", "33"]
    with raises(ValueError):
        get_move(available_move, "00")


def test_register_move():
    player = Player("Player1", "O")
    opponent = Player("Player2", "X")
    board = Board(3)
    winning_pattern = [
        ["11", "22", "33"],
        ["11", "12", "13"],
        ["22", "23", "24"]
    ]
    register_move("11", player, opponent, board, winning_pattern)
    assert winning_pattern == [["22", "23", "24"]]
    assert player.player_winning_patterns == [["11", "22", "33"], ["11", "12", "13"]]
    register_move("12", opponent, player, board, winning_pattern)
    assert player.player_winning_patterns == [["11", "22", "33"]]
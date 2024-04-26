__author__ = "Ellen Whalen"
"""Tests for the lines_of_action class."""

from lines_of_action import LinesOfAction
import pytest

def test_simple_search():
    my_game = LinesOfAction()
    # This will just return the first piece (of the correct color) that it comes upon.
    assert my_game.simple_search("X") == (0, 1)
    assert my_game.simple_search("O") == (1, 0)

def test_dfs():
    my_game = LinesOfAction()
    visited = []
    my_game.dfs((0, 1), visited)
    assert visited == [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
    visited = []
    my_game.dfs((1, 7), visited)
    assert visited == [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
    my_game.board.move_piece(0, 1, 0, 7) 
    # Checking that dfs doesn't add the black piece I just moved to visited
    my_game.dfs((1, 7), visited)
    assert visited == [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
    with pytest.raises(ValueError) as excinfo:  
        my_game.dfs((0, 0), visited)
    assert str(excinfo.value) == "Can't search on a piece that doesn't exist."
    # More checks on test_dfs are inherently run by test_check_board() (because it calls dfs)

def test_check_board():
    my_game = LinesOfAction()
    wins = my_game.check_board()
    assert wins["x_win"] == False
    assert wins["o_win"] == False
    my_game.board.move_piece(0, 1, 6, 1)
    my_game.board.move_piece(0, 2, 6, 2)
    my_game.board.move_piece(0, 3, 6, 3)
    my_game.board.move_piece(0, 4, 6, 4)
    my_game.board.move_piece(0, 5, 6, 5)
    my_game.board.move_piece(0, 6, 6, 6)
    wins = my_game.check_board()
    assert wins["x_win"] == True
    assert wins["o_win"] == False
    my_game.board.move_piece(1, 7, 1, 1)
    my_game.board.move_piece(2, 7, 2, 1)
    my_game.board.move_piece(3, 7, 3, 1)
    my_game.board.move_piece(4, 7, 4, 1)
    my_game.board.move_piece(5, 7, 5, 1)
    my_game.board.move_piece(6, 7, 6, 1)
    wins = my_game.check_board()
    assert wins["x_win"] == True
    assert wins["o_win"] == True
    my_game.board.move_piece(1, 1, 1, 2)
    wins = my_game.check_board()
    assert wins["x_win"] == True
    assert wins["o_win"] == True
    my_game.board.move_piece(1, 2, 1, 3)
    wins = my_game.check_board()
    assert wins["x_win"] == True
    assert wins["o_win"] == False


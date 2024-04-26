__author__ = "Ellen Whalen"


import pytest
from board import Board

def test_move_piece():
    my_board = Board()
    my_board.move_piece(0, 1, 1, 1)
    assert my_board.grid[0][1] == ""
    assert my_board.grid[1][1] == "X"
    # "Capturing" the black piece on 1 1
    my_board.move_piece(1, 0, 1, 1)
    assert my_board.grid[1][0] == ""
    assert my_board.grid[1][1] == "O"
    with pytest.raises(ValueError) as excinfo:  
        my_board.move_piece(0, 1, 1, 1)
    assert str(excinfo.value) == "Can't move a piece that doesn't exist."

def test_count_pieces():
    my_board = Board()
    counts = my_board.count_pieces(7, 3)
    assert counts["row_count"] == 6
    assert counts["col_count"] == 2
    assert counts["neg_diag_count"] == 2
    assert counts["pos_diag_count"] == 2
    counts = my_board.count_pieces(4, 7)
    assert counts["row_count"] == 2
    assert counts["col_count"] == 6
    assert counts["neg_diag_count"] == 2
    assert counts["pos_diag_count"] == 2
    with pytest.raises(ValueError) as excinfo:  
        counts = my_board.count_pieces(1, 1)
    assert str(excinfo.value) == "count_pieces should not be run on an empty square."

def test_count_total():
    my_board = Board()
    assert my_board.count_total("X") == 12
    assert my_board.count_total("O") == 12
    my_board._grid[1][0] = ""
    my_board._grid[4][0] = ""
    my_board._grid[0][3] = ""
    my_board._grid[7][6] = ""
    my_board._grid[1][7] = ""
    assert my_board.count_total("X") == 10
    assert my_board.count_total("O") == 9

def test_find_moves():
    # This tests find_moves and find_row_moves, find_col_moves, find_neg_diag_moves, and find_pos_diag_moves. Pretty much
    # all that find_moves does is find some basic data about the square and then call all of those methods.
    my_board = Board()
    with pytest.raises(ValueError) as excinfo:  
        my_board.find_moves(0, 7)
    assert str(excinfo.value) == "Can't find moves for a piece that doesn't exist."
    moves = my_board.find_moves(0, 6)
    assert moves == [(0, 0), (2, 6), (2, 4)]
    my_board.move_piece(1, 7, 1, 6)
    moves = my_board.find_moves(0, 6)
    # Can no longer move along the column - it's blocked by a black piece.
    # But can move along the diagonal!
    assert moves == [(0, 0), (1, 7), (2, 4)]
    my_board.move_piece(6, 7, 3, 4)
    moves = my_board.find_moves(3, 4)
    assert moves == [(3, 1), (6, 4), (0, 4), (5, 6), (1, 2), (5, 2)]
   


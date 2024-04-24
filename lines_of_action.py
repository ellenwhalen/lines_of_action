__author__ = "Ellen Whalen"

import graphics as g

class Board:
    
    def __init__(self):
        self._grid = []
        for i in range(DIM):
            self._grid.append([""] * DIM)
        for i in range(1, 7):
            self._grid[0][i] = "X"
            self._grid[7][i] = "X"
            self._grid[i][0] = "O"
            self._grid[i][7] = "O"
    
    @property
    def grid(self):
        return self._grid
    
    def count_pieces(self, row: int, col: int) -> dict:
        if self.grid[row][col] == "":
            raise ValueError("count_pieces should not be run on an empty square.")
        counts = {"row_count": 0,
                 "col_count": 0,
                 "neg_diag_count": 0,
                 "pos_diag_count": 0}
        i = 0
        while i < DIM:
            if self.grid[row][i] != "":
                counts["row_count"] += 1
            i += 1

        i = 0
        while i < DIM:
            if self.grid[i][col] != "":
                counts["col_count"] += 1
            i += 1
            
        i = row 
        j = col
        while i > 0 and j > 0:
            # getting i and j to the "start" of the diagonal running from L-top to R-bottom (-x direction)
            i -= 1
            j -= 1
        while i < DIM and j < DIM:
            if self.grid[i][j] != "":
                counts["neg_diag_count"] += 1
            i += 1
            j += 1

        i = row
        j = col
        while i < DIM - 1 and j > 0:
            # getting i and j to the "start" of the diagonal running from L-bottom to R-top (+x direction)
            i += 1
            j -= 1
        while i >= 0 and j < DIM:
            if self.grid[i][j] != "":
                counts["pos_diag_count"] += 1
            i -= 1
            j += 1
        return counts

    def move_piece(self, row: int, col: int, new_row: int, new_col: int):
        color_type = self._grid[row][col]
        self._grid[row][col] = ""
        self._grid[new_row][new_col] = color_type
        print(self._grid)
    

class LinesOfAction:
    _is_black_turn: bool
    _board: Board
    _win: g.GraphWin

    def __init__(self):
        self._is_black_turn = True
        self._board = Board()
        self._win = g.GraphWin("Lines of Action", 800, 800)
        self._win.setBackground("mediumseagreen")
        self._win.setCoords(0, DIM, DIM, 0)

    @property
    def is_black_turn(self):
        return self._is_black_turn
    
    @property
    def board(self):
        return self._board
    
    @property 
    def win(self):
        return self._win
    
    def draw_board(self):
        for i in range(DIM):
            line = g.Line(g.Point(0, i), g.Point(DIM, i))
            line.draw(self.win)
            line = g.Line(g.Point(i, 0), g.Point(i, DIM))
            line.draw(self.win)
        for i in range(DIM):
            for j in range(DIM):
                if self.board.grid[i][j] == "X":
                    circle = g.Circle(g.Point(j + 0.5, i + 0.5), 0.25)
                    circle.setFill("black")
                    circle.draw(self.win)
                if self.board.grid[i][j] == "O":
                    circle = g.Circle(g.Point(j + 0.5, i + 0.5), 0.25)
                    circle.setFill("white")
                    circle.draw(self.win)

    def find_moves(self, row: int, col: int) -> list[tuple]:
        color = self.board.grid[row][col]
        if color == "X":
            opponent = "O"
        else:
            opponent = "X"
        counts = self.board.count_pieces(row, col)
        moves = []
        moves += self.find_row_moves(row, col, color, opponent, counts["row_count"])
        moves += self.find_col_moves(row, col, color, opponent, counts["col_count"])
        moves += self.find_neg_diag_moves(row, col, color, opponent, counts["neg_diag_count"])
        moves += self.find_pos_diag_moves(row, col, color, opponent, counts["pos_diag_count"])
        return moves
    
    def find_row_moves(self, row: int, col: int, color: str, opponent: str, count: int) -> list[tuple]:
        moves = []

        can_move = True
        i = 1
        col_check = col + 1
        while col_check < DIM and i < count and can_move:
            if self.board.grid[row][col_check] == opponent:
                can_move = False
            i += 1
            col_check += 1

        # lots of logic that gets repeated, so i'll explain it once here.
        # if the loop was able to get all the way to the distance the piece would need to travel,
        if i == count:    
            # if the reason the while loop ended WASN'T because col_check overspills bounds,
            if col_check < DIM:     
                # if the spot the piece would land on is the same color as itself,
                if self.board.grid[row][col_check] == color:
                    can_move = False    # the piece can't move there.
            # otherwise if col_check DID overspill bounds,
            else:   
                can_move = False    # the piece can't move there. (obviously)
            # if the piece can STILL move,
            if can_move:
                moves += [(row, col_check)]
        
        can_move = True
        i = 1
        col_check = col - 1
        while col_check > 0 and i < count and can_move:
            if self.board.grid[row][col_check] == opponent:
                can_move = False
            i += 1
            col_check -= 1

        if i == count:
            if col_check >= 0:
                if self.board.grid[row][col_check] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row, col_check)]
        return moves
    
    def find_col_moves(self, row: int, col: int, color: str, opponent: str, count: int):
        moves = []
        can_move = True
        i = 1
        row_check = row + 1
        while row_check < DIM and i < count and can_move:
            if self.board.grid[row_check][col] == opponent:
                can_move = False
            i += 1
            row_check += 1

        if i == count:
            if row_check < DIM:
                if self.board.grid[row_check][col] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col)]
        
        can_move = True
        i = 1
        row_check = row - 1
        while row_check > 0 and i < count and can_move:
            if self.board.grid[row_check][col] == opponent:
                can_move = False
            i += 1
            row_check -= 1
        
        if i == count:
            if row_check >= 0:
                if self.board.grid[row_check][col] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col)]
        return moves
    
    def find_neg_diag_moves(self, row: int, col: int, color: str, opponent: str, count: int):
        moves = []
        can_move = True
        i = 1
        col_check = col + 1
        row_check = row + 1
        while col_check < DIM and row_check < DIM and i < count and can_move:
            if self.board.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check += 1
            row_check += 1

        if i == count:
            if col_check < DIM and row_check < DIM:
                if self.board.grid[row_check][col_check] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col_check)]
        
        can_move = True
        i = 1
        col_check = col - 1
        row_check = row - 1
        while col_check > 0 and row_check > 0 and i < count and can_move:
            if self.board.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check -= 1
            row_check -= 1
        
        if i == count:
            if col_check >= 0 and row_check >= 0:
                if self.board.grid[row_check][col_check] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col_check)]
        return moves
    
    def find_pos_diag_moves(self, row: int, col: int, color: str, opponent: str, count: int):
        moves = []
        can_move = True
        i = 1
        col_check = col + 1
        row_check = row - 1
        while col_check < DIM and row_check > 0 and i < count and can_move:
            if self.board.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check += 1
            row_check -= 1

        if i == count:
            if col_check < DIM and row_check >= 0:
                if self.board.grid[row_check][col_check] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col_check)]
        
        can_move = True
        i = 1
        col_check = col - 1
        row_check = row + 1
        while col_check > 0 and row_check < DIM and i < count and can_move:
            if self.board.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check -= 1
            row_check += 1
        
        if i == count:
            if col_check >= 0 and row_check < DIM:
                if self.board.grid[row_check][col_check] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col_check)]
        return moves

    def show_possible_moves(self, moves: list[tuple]):
        length = len(moves)
        for i in range(length):
            row = moves[i][0]
            col = moves[i][1]
            rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row)) # could change these to like. grayed out circles
            rect.setFill("greenyellow")
            rect.draw(self.win)
            if self.board.grid[row][col] != "":
                color_type = self.board.grid[row][col]
                if color_type == "X":
                    color = "black"
                else:
                    color = "white"
                circle = g.Circle(g.Point(col + 0.5, row + 0.5), 0.25)
                circle.setFill(color)
                circle.draw(self.win)
    
    def select_piece(self, row: int, col: int, moves: list[tuple]):
        rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row)) # could change these to like. grayed out circles
        rect.setFill("palegreen")
        rect.draw(self.win)
        color_type = self.board.grid[row][col]
        if color_type == "X":
            color = "black"
        else:
            color = "white"
        circle = g.Circle(g.Point(col + 0.5, row + 0.5), 0.25)
        circle.setFill(color)
        circle.draw(self.win)
        self.show_possible_moves(moves)
    
    def unselect_piece(self, row: int, col: int, moves: list[tuple]):
        rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row)) # could change these to like. grayed out circles
        rect.setFill("mediumseagreen")
        rect.draw(self.win)
        color_type = self.board.grid[row][col]
        if color_type == "X":
            color = "black"
        else:
            color = "white"
        circle = g.Circle(g.Point(col + 0.5, row + 0.5), 0.25)
        circle.setFill(color)
        circle.draw(self.win)
        length = len(moves)
        for i in range(length):
            row = moves[i][0]
            col = moves[i][1]
            rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row)) # could change these to like. grayed out circles
            rect.setFill("mediumseagreen")
            rect.draw(self.win)
            if self.board.grid[row][col] != "":
                color_type = self.board.grid[row][col]
                if color_type == "X":
                    color = "black"
                else:
                    color = "white"
                circle = g.Circle(g.Point(col + 0.5, row + 0.5), 0.25)
                circle.setFill(color)
                circle.draw(self.win)      

    def show_move(self):
        for i in range(DIM):
            for j in range(DIM):
                if self.board.grid[i][j] == "X":
                    circle = g.Circle(g.Point(j + 0.5, i + 0.5), 0.25)
                    circle.setFill("black")
                    circle.draw(self.win)
                elif self.board.grid[i][j] == "O":
                    circle = g.Circle(g.Point(j + 0.5, i + 0.5), 0.25)
                    circle.setFill("white")
                    circle.draw(self.win)
                else:
                    rect = g.Rectangle(g.Point(j + 1, i + 1), g.Point(j, i))
                    rect.setFill("mediumseagreen")
                    rect.draw(self.win)

    def play_game(self):
        self.draw_board()
        game_running = True
        while game_running:
            if self.is_black_turn:
                click = self.win.getMouse()
                row = int(click.getY())
                col = int(click.getX())
                while self.board.grid[row][col] == "X":
                    moves = self.find_moves(row, col)
                    self.select_piece(row, col, moves)
                    x_selected = (row, col)
                    click = self.win.getMouse()
                    self.unselect_piece(row, col, moves)
                    row = int(click.getY())
                    col = int(click.getX())
                possible_move = (row, col)
                i = 0
                has_not_moved = True
                while i < len(moves) and has_not_moved:
                    if possible_move == moves[i]:
                        self.board.move_piece(x_selected[0], x_selected[1], moves[i][0], moves[i][1])
                        self.show_move()
                        has_not_moved = False
                        self._is_black_turn = False
                    i += 1
            
            if not self.is_black_turn:
                click = self.win.getMouse()
                row = int(click.getY())
                col = int(click.getX())
                while self.board.grid[row][col] == "O":
                    moves = self.find_moves(row, col)
                    self.select_piece(row, col, moves)
                    o_selected = (row, col)
                    click = self.win.getMouse()
                    self.unselect_piece(row, col, moves)
                    row = int(click.getY())
                    col = int(click.getX())
                possible_move = (row, col)
                i = 0
                has_not_moved = True
                while i < len(moves) and has_not_moved:
                    if possible_move == moves[i]:
                        self.board.move_piece(o_selected[0], o_selected[1], moves[i][0], moves[i][1])
                        self.show_move()
                        has_not_moved = False
                        self._is_black_turn = True
                    i += 1
        
    
        
DIM = 8

my_board = Board()
print(my_board.count_pieces(4, 0))

my_game = LinesOfAction()
#my_game.draw_board()
my_game.play_game()
my_game.win.getMouse()
my_game.win.close()

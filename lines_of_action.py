__author__ = "Ellen Whalen"

import graphics as g
from box import Box

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
        """Counts the number of pieces on a given piece's row, column, and both diagonals."""
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
        """Moves a piece from [row][col] to [new_row][new_col]."""
        if self.grid[row][col] == "":
            raise ValueError("Can't move a piece that doesn't exist.")
        color_type = self._grid[row][col]
        self._grid[row][col] = ""
        self._grid[new_row][new_col] = color_type
    
    def count_x(self) -> int:
        count = 0
        for i in range(DIM):
            for j in range(DIM):
                if self.grid[j][i] == "X":
                    count += 1
        return count
    
    def count_o(self) -> int:
        count = 0
        for i in range(DIM):
            for j in range(DIM):
                if self.grid[j][i] == "O":
                    count += 1
        return count

class LinesOfAction:
    _is_black_turn: bool
    _board: Board
    _win: g.GraphWin

    def __init__(self):
        self._is_black_turn = True
        self._board = Board()
        self._win = g.GraphWin("Lines of Action", 800, 800, autoflush=False)
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
        """Draws the board in its initial state."""
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
        self.win.update()

    def find_moves(self, row: int, col: int) -> list[tuple]:
        """Finds possible moves for a piece and returns them as a list of tuples (row, col)."""
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
        """Finds possible moves for a piece along its row."""
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
        """Finds possible moves for a piece along its column."""
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
        """Finds possible moves for a piece along its diagonal going from the upper left to lower right."""
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
        """Finds possible moves for a piece along the diagonal going from its lower left to upper right."""
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
        """Displays possible moves as light green squares."""
        length = len(moves)
        for i in range(length):
            row = moves[i][0]
            col = moves[i][1]
            rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row))
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
        self.win.update()
    
    def select_piece(self, row: int, col: int, moves: list[tuple]):
        """Selects a piece, calculates its possible moves and displays them."""
        rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row))
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
        self.win.update()
    
    def unselect_piece(self, row: int, col: int, moves: list[tuple]):
        """Deselects a piece which has previously been selected."""
        rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row))
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
        self.win.update()

    def show_move(self):
        """Called after a piece is moved. Updates the board to show that move."""
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
        self.win.update()

    def play_game(self):
        self.draw_board()
        game_running = True
        while game_running:
            round = True
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
                        round = False
                    i += 1
            if not round:
                self.check_board()
        
    def check_board(self):
        x_win = False
        o_win = False
        x_count = self.board.count_x()
        o_count = self.board.count_o()
        # search for an x and an o on the board. we only need to search for two.
        i = 0
        searching = True
        while i < DIM and searching:
            j = 0
            while j < DIM and searching:
                if self.board.grid[i][j] == "X":
                    x_vertex = (i, j)
                    searching = False
                j += 1
            i += 1
        
        i = 0
        searching = True
        while i < DIM and searching:
            j = 0
            while j < DIM and searching:
                if self.board.grid[i][j] == "O":
                    o_vertex = (i, j)
                    searching = False
                j += 1
            i += 1

        x_visited = []
        o_visited = []
        self.dfs(x_vertex, x_visited)
        self.dfs(o_vertex, o_visited)
        print(x_visited)
        print(o_visited)

        if len(x_visited) == x_count:
            x_win = True
        if len(o_visited) == o_count:
            o_win = True
        print(x_win)
        print(o_win)

    def dfs(self, vertex: tuple, visited: list):
        if vertex not in visited:
            visited.append(vertex)
            box = Box(vertex[0], vertex[1], DIM)
            for i in box.row_range():
                for j in box.col_range():
                    if self.board.grid[i][j] == self.board.grid[vertex[0]][vertex[1]]:
                        self.dfs((i, j), visited)

        

DIM = 8

my_board = Board()
print(my_board.count_pieces(4, 0))

my_game = LinesOfAction()
#visited = []
#my_game.dfs((1, 0), visited)
#print(visited)
my_game.play_game()
my_game.win.getMouse()
my_game.win.close()

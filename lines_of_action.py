
__author__ = "Ellen Whalen"
"""Class for the game functions of Lines Of Action."""

import graphics as g
from box import Box
from board import Board

class LinesOfAction:
    """An object which runs one game of Lines of Action, finding and executing moves, controlling graphics, 
    and checking for wins."""
    _round: bool
    _board: Board
    _win: g.GraphWin

    def __init__(self):
        self._is_black_turn = True
        self._round = True
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
        # Drawing all of the gridlines
        for i in range(DIM):
            line = g.Line(g.Point(0, i), g.Point(DIM, i))
            line.draw(self.win)
            line = g.Line(g.Point(i, 0), g.Point(i, DIM))
            line.draw(self.win)
        # Drawing all of the pieces
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

    def show_possible_moves(self, moves: list[tuple]):
        """Displays possible moves as light green squares."""
        length = len(moves)
        for i in range(length):
            row = moves[i][0]
            col = moves[i][1]
            # Changing background colors
            rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row))
            rect.setFill("greenyellow")
            rect.draw(self.win)
            # Redrawing pieces on top
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
        """Selects a piece, checks its possible moves and displays them."""
        # Changes the background behind the selected piece to a lighter shade of green.
        rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row))
        rect.setFill("palegreen")
        rect.draw(self.win)

        # Redraws the piece on top of it.
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
    
    def deselect_piece(self, row: int, col: int, moves: list[tuple]):
        """Deselects a piece which has previously been selected."""

        # Turns the square of the selected piece back to the normal shade of green.
        rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row))
        rect.setFill("mediumseagreen")
        rect.draw(self.win)
        color_type = self.board.grid[row][col]
        if color_type == "X":
            color = "black"
        else:
            color = "white"
        
        # Redraws the piece on top of the square.
        circle = g.Circle(g.Point(col + 0.5, row + 0.5), 0.25)
        circle.setFill(color)
        circle.draw(self.win)

        # Redraws the rest of the board.
        length = len(moves)
        for i in range(length):
            row = moves[i][0]
            col = moves[i][1]
            rect = g.Rectangle(g.Point(col + 1, row + 1), g.Point(col, row))
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
        """Controls the gameplay, letting the correct pieces move and calling checks for wins."""
        self.draw_board()
        game_running = True
        while game_running:
            self._round = True
            if self.is_black_turn:
                self.take_turn("X")
            if not self.is_black_turn:
                self.take_turn("O")

            if not self._round:
                # Every time a round ends, check to see if either/both win conditions are met and respond accordingly.
                win_conditions = self.check_board()
                if win_conditions["x_win"] and win_conditions["o_win"]:
                    print("---THE GAME HAS ENDED---")
                    print("It's a draw!")
                    game_running = False
                elif win_conditions["x_win"]:
                    print("---THE GAME HAS ENDED---")
                    print("Black wins!")
                    game_running = False
                elif win_conditions["o_win"]:
                    print("---THE GAME HAS ENDED---")
                    print("White wins!")
                    game_running = False
        self.win.getMouse()
        self.win.close()

    def take_turn(self, color: str):
        """Allows one turn to be taken for either color of a piece."""
        moves = []
        click = self.win.getMouse()
        # Getting the row and column info from the getMouse object (click)
        row = int(click.getY())
        col = int(click.getX())
        # Functions as an if statement, but needs to be a while because the player can select one piece,
        # then another piece, etc
        while self.board.grid[row][col] == color:
            # Calculating possible moves
            moves = self.board.find_moves(row, col)
            # Selecting the piece based on said moves
            self.select_piece(row, col, moves)
            x_selected = (row, col)
            # Waiting for the user's next click
            click = self.win.getMouse()
            # Deselecting the piece
            self.deselect_piece(row, col, moves)
            row = int(click.getY())
            col = int(click.getX())

        # Checking the possible move (user's click) against all possible moves
        possible_move = (row, col)
        i = 0
        has_not_moved = True
        while i < len(moves) and has_not_moved: 
            if possible_move == moves[i]:
                self.board.move_piece(x_selected[0], x_selected[1], moves[i][0], moves[i][1])
                self.show_move()
                has_not_moved = False
                # Inverting the turn
                self._is_black_turn = not self._is_black_turn
                if color == "O":
                    # If it was white's turn, the round is now over since white has moved.
                    self._round = False
            i += 1
        
    def check_board(self):
        """Checks the board to see if any end condition is met, then returns whether there is a win for black and/or white."""
        x_win = False
        o_win = False
        x_count = self.board.count_total("X")
        o_count = self.board.count_total("O")

        # search for an x and an o on the board. we only need to get the first two we come upon.
        x_vertex = self.simple_search("X")
        o_vertex = self.simple_search("O")

        x_visited = []
        o_visited = []
        # dfs based on a starting vertex given by simple_search
        self.dfs(x_vertex, x_visited)
        self.dfs(o_vertex, o_visited)
        

        if len(x_visited) == x_count:
            x_win = True
        if len(o_visited) == o_count:
            o_win = True
        return {"x_win": x_win,
                "o_win": o_win}
        
    def simple_search(self, color):
        """Searches the board until it finds the right color piece."""
        i = 0
        while i < DIM:
            j = 0
            while j < DIM:
                if self.board.grid[i][j] == color:
                    vertex = (i, j)
                    return vertex
                j += 1
            i += 1

    def dfs(self, vertex: tuple, visited: list):
        """Depth-first search for pieces of some particular color on the board."""
        if self.board.grid[vertex[0]][vertex[1]] == "":
            raise ValueError("Can't search on a piece that doesn't exist.")
        if vertex not in visited:
            visited.append(vertex)
            box = Box(vertex[0], vertex[1], DIM)
            for i in box.row_range():
                for j in box.col_range():
                    # self.board.grid[vertex[0]][vertex[1]] returns the color of the piece we want to run dfs on.
                    if self.board.grid[i][j] == self.board.grid[vertex[0]][vertex[1]]:
                        self.dfs((i, j), visited)
        

DIM = 8     # I'm using this as a constant not because it should change, but because it's easier to read.

# !!!!!!YOU NEED TO COMMENT OUT THE FOLLOWING TWO LINES FOR THE TESTS ON THIS FILE TO RUN!!!!!!
"""
my_game = LinesOfAction()
my_game.play_game()
"""
my_game = LinesOfAction()
bla = []
my_game.dfs((1, 0), bla)
print(bla)
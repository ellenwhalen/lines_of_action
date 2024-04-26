DIM = 8

class Board: 
    """A list representing the game board with black pieces as "X"'s and white pieces as "O"'s 
    which can run some basic operations on itself."""
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
        
        # initializing counts, a dict that will hold all of the counts
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
    
    def count_total(self, color: str) -> int:
        count = 0
        for i in range(DIM):
            for j in range(DIM):
                if self.grid[j][i] == color:
                    count += 1
        return count

    def find_moves(self, row: int, col: int) -> list[tuple]:
        """Finds possible moves for a piece and returns them as a list of tuples (row, col)."""
        if self.grid[row][col] == "":
            raise ValueError("Can't find moves for a piece that doesn't exist.")
        color = self.grid[row][col]
        if color == "X":
            opponent = "O"
        else:
            opponent = "X"
        counts = self.count_pieces(row, col)

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
            if self.grid[row][col_check] == opponent:
                can_move = False
            i += 1
            col_check += 1

        # LOTS of logic that gets repeated in all of these "find_[something]_moves" methods, so i'll explain it once here.
        # if the loop was able to get all the way to the distance the piece would need to travel,
        if i == count:    
            # if the reason the while loop ended WASN'T because col_check overspills bounds,
            if col_check < DIM:     
                # if the spot the piece would land on is the same color as itself,
                if self.grid[row][col_check] == color:
                    can_move = False    # the piece can't move there.
            # otherwise if col_check DID overspill bounds,
            else:   
                can_move = False    # the piece can't move there. (obviously)
            # if the piece can STILL move to that space,
            if can_move:
                # add that move to the array of possible moves.
                moves += [(row, col_check)]
        
        can_move = True
        i = 1
        col_check = col - 1
        while col_check > 0 and i < count and can_move:
            if self.grid[row][col_check] == opponent:
                can_move = False
            i += 1
            col_check -= 1

        if i == count:
            if col_check >= 0:
                if self.grid[row][col_check] == color:
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
            if self.grid[row_check][col] == opponent:
                can_move = False
            i += 1
            row_check += 1

        if i == count:
            if row_check < DIM:
                if self.grid[row_check][col] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col)]
        
        can_move = True
        i = 1
        row_check = row - 1
        while row_check > 0 and i < count and can_move:
            if self.grid[row_check][col] == opponent:
                can_move = False
            i += 1
            row_check -= 1
        
        if i == count:
            if row_check >= 0:
                if self.grid[row_check][col] == color:
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
            if self.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check += 1
            row_check += 1

        if i == count:
            if col_check < DIM and row_check < DIM:
                if self.grid[row_check][col_check] == color:
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
            if self.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check -= 1
            row_check -= 1
        
        if i == count:
            if col_check >= 0 and row_check >= 0:
                if self.grid[row_check][col_check] == color:
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
            if self.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check += 1
            row_check -= 1

        if i == count:
            if col_check < DIM and row_check >= 0:
                if self.grid[row_check][col_check] == color:
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
            if self.grid[row_check][col_check] == opponent:
                can_move = False
            i += 1
            col_check -= 1
            row_check += 1
        
        if i == count:
            if col_check >= 0 and row_check < DIM:
                if self.grid[row_check][col_check] == color:
                    can_move = False
            else:
                can_move = False
            if can_move:
                moves += [(row_check, col_check)]
        return moves

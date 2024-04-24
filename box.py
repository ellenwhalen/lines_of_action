class Box:
    _min_row = int
    _max_row = int
    _min_col = int
    _max_col = int

    def __init__(self, row: int, col: int, dim: int):
        self._min_row = max(0, row - 1)
        self._max_row = min(dim - 1, row + 1)
        self._min_col = max(0, col - 1)
        self._max_col = min(dim - 1, col + 1)
    
    @property
    def min_row(self):
        return self._min_row
    
    @property
    def max_row(self):
        return self._max_row
    
    @property
    def min_col(self):
        return self._min_col
    
    @property
    def max_col(self):
        return self._max_col
    
    def row_range(self):   
        """Returns the range from min_row to max_row."""
        return range(self.min_row, self.max_row + 1)
    
    def col_range(self):
        """Returns the range from min_col to max_col."""
        return range(self.min_col, self.max_col + 1)
    
    def total_range(self):
        """Returns the total number of squares in the Box."""
        total = 0
        for i in self.row_range():
            for j in self.col_range():
                total += 1
        return total
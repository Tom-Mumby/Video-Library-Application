class ArrayPoint:
    """Contains row and column information and methods to act on these"""

    def __init__(self, column, row):
        """Sets initial values for the column and row"""
        self.column = column
        self.row = row

    def get_product(self):
        return self.column * self.row

    def set(self, point):
        """set new values"""
        self.column = point.column
        self.row = point.row

    def print_out(self):
        print("Column:  " + str(self.column))
        print("Row:  " + str(self.row))
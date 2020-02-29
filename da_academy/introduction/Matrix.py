class Row:
    def __init__(self, length):
        self._row = [0 for _ in range(length)]

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        if not isinstance(row, list):
            raise TypeError('unsupported type')
        if len(self._row) != len(row):
            raise ValueError('rows are not the same dimension')
        self._row = row

    def __getitem__(self, item):
        return self.row[item]

    def __add__(self, other):
        if not isinstance(other, Row):
            raise TypeError('unsupported operand type')
        if len(self.row) != len(other.row):
            raise ValueError('rows are not the same dimension')
        row = self.row
        other_row = other.row
        return [row[i] + other_row[i] for i in range(0, len(row))]

    def __len__(self):
        return len(self.row)

    def __repr__(self):
        return 'Row {}'.format(self.row)


class Matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = [Row(columns) for _ in range(rows)]

    def __getitem__(self, item):
        return self.matrix[item]

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('unsupported operand type')
        if self.rows != other.rows:
            raise ValueError('matrices are not the same dimension')
        return [self.matrix[i] + other[i] for i in range(0, len(self.matrix))]


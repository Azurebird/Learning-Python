class Row:
    def __init__(self, items):
        self.length = len(items)
        self.row = items

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        if not isinstance(row, list):
            raise TypeError('unsupported type')
        if self.length != len(row):
            raise ValueError('rows are not the same length')
        self._row = row

    def __getitem__(self, item):
        return self.row[item]

    def __add__(self, other):
        if not isinstance(other, Row):
            raise TypeError('unsupported operand type')
        if self.length != len(other.row):
            raise ValueError('rows are not the same dimension')
        row = self.row
        other_row = other.row
        return [row[i] + other_row[i] for i in range(0, len(row))]

    def __len__(self):
        return len(self.row)

    def __repr__(self):
        return 'Row {}'.format(self.row)

    def __str__(self):
        return str(self.row)


class Matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = [Row([0 for _ in range(columns)]) for _ in range(rows)]

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        if not isinstance(value, Row):
            raise TypeError('unsupported operand type')
        if self.columns != len(value):
            raise ValueError('rows are not the same dimension')
        self.matrix[key] = value

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('unsupported operand type')
        if self.rows != other.rows:
            raise ValueError('matrices are not the same dimension')
        return [self.matrix[i] + other[i] for i in range(0, self.columns)]

    def __repr__(self):
        return 'Matrix {}'.format([repr(self.matrix[x]) for x in range(self.columns)])

    def __str__(self):
        return str([str(self.matrix[x]) for x in range(self.columns)])

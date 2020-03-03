import copy

class Matrix:
    def __init__(self, base_matrix):
        base_column_len = len(base_matrix[0])
        for row in base_matrix:
            if len(row) != base_column_len:
                raise ValueError('not all rows have the same length')
        self.rows = len(base_matrix)
        self.columns = base_column_len
        self.matrix = base_matrix

    def __eq__(self, other):
        return self.matrix == other.matrix

    def __copy__(self):
        return Matrix([row.copy() for row in self.matrix])

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        if not isinstance(value, list):
            raise TypeError('unsupported operand type')
        if self.columns != len(value):
            raise ValueError('rows are not the same dimension')
        self.matrix[key] = value

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('unsupported operand type')
        if self.rows != other.rows:
            raise ValueError('matrices are not the same dimension')
        return Matrix([[self.matrix[i][j] + other[i][j] for j in range(self.rows)] for i in range(self.columns)])

    def __mul__(self, other):
        """
        Operates the multiplication of two matrices with a naive complexity of O(n^3)
        :param other: The matrix to multiply with this one
        :return: A new matrix equals to the multiplication of self and other
        """
        number_columns = len(other[0])
        return Matrix([
            [
                sum([
                    row[x] * other.__get_column(j)[x] for x in range(len(row))
                ]) for j in range(number_columns)
            ] for i, row in enumerate(self.matrix)
        ])

    def __repr__(self):
        return 'Matrix {}'.format([repr(self.matrix[x]) for x in range(self.columns)])

    def __str__(self):
        return str([str(self.matrix[x]) for x in range(self.columns)])

    def __is_square(self):
        return self.columns == self.rows

    def __delete_row(self, row):
        self.rows -= 1
        del self.matrix[row]

    def __delete_column(self, column):
        self.columns -= 1
        for row in self.matrix:
            del row[column]

    def __minor(self, i, j):
        m = copy.copy(self)
        m.__delete_row(i)
        m.__delete_column(j)
        return m.determinant()

    def __cofactor(self, row, column):
        if not self.__is_square():
            raise ValueError("square matrix required")
        return ((-1) ** (row + column)) * self.__minor(row, column)

    def __cofactor_matrix(self):
        return Matrix([[self.__cofactor(i, j) for j in range(self.columns)] for i in range(self.rows)])

    def __get_column(self, column):
        return [row[column] for row in self.matrix]

    def get_multiple_rows(self, *rows):
        return [self.matrix[row] for row in rows]

    def scalar_mul(self, scalar):
        return Matrix([[self.matrix[i][j] * scalar for j in range(self.columns)] for i in range(self.rows)])

    def transpose(self):
        return Matrix([[self.matrix[row][column] for row in range(self.rows)] for column in range(self.columns)])

    def determinant(self):
        """
        Based on the code of Thom Ives: Data Scientist, PhD multi-physics engineer, and python
        :return: The determinant of this matrix
        """
        triangular_matrix = copy.copy(self)
        for fd in range(self.rows):
            for i in range(fd + 1, self.rows):
                if triangular_matrix[fd][fd] == 0:
                    triangular_matrix[fd][fd] = 1.0e-18
                cr_scalar = triangular_matrix[i][fd] / triangular_matrix[fd][fd]
                for j in range(self.rows):
                    triangular_matrix[i][j] = triangular_matrix[i][j] - cr_scalar * triangular_matrix[fd][j]

        product = 1.0
        for i in range(self.rows):
            product *= triangular_matrix[i][i]

        return round(product)

    def adjugate(self):
        return self.__cofactor_matrix().transpose()

    def inverse(self):
        if self.determinant() == 0:
            raise ValueError('Matrix is not invertible')
        return self.adjugate().scalar_mul(1 / self.determinant())

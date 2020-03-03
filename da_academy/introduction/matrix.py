import copy
from collections import OrderedDict


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
        self.__is_same_dimension(other)
        return Matrix([[self.matrix[i][j] + other[i][j] for j in range(self.rows)] for i in range(self.columns)])

    def __mul__(self, other):
        self.__is_instance(other)
        if self.columns != other.rows:
            raise ValueError('matrices cant be multiplied between them')
        number_columns = len(other[0])
        return Matrix([
            [
                sum([
                    row[x] * other.get_column(j)[x] for x in range(len(row))
                ]) for j in range(number_columns)
            ] for i, row in enumerate(self.matrix)
        ])

    def __repr__(self):
        return 'Matrix {}'.format([repr(self.matrix[x]) for x in range(self.rows)])

    def __str__(self):
        return str([str(self.matrix[x]) for x in range(self.columns)])

    def __is_instance(self, other):
        """
        Checks if other is an instance of self if its not a TypeError is raised
        :param other: The matrix to compare with self
        """
        if type(self) != type(other):
            raise TypeError('unsupported operand type')

    def __is_same_dimension(self, other):
        """
        Checks if other is has the same dimension as self if its not a TypeError is raised
        :param other: The matrix to compare with self
        """
        self.__is_instance(other)
        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError('matrices are not the same dimension')

    def __is_square(self):
        """
        Tells if this Matrix is square, that's number of rows equal to number of columns
        :return: true if this matrix is square
        """
        return self.columns == self.rows

    def __delete_row(self, row):
        """
        Deletes a row in the specified index
        :param row: The row index to delete
        """
        self.rows -= 1
        del self.matrix[row]

    def __delete_column(self, column):
        """
        Deletes a column in the specified index
        :param column: The column index to delete
        """
        self.columns -= 1
        for row in self.matrix:
            del row[column]

    def __minor(self, i, j):
        """
        Determinant of the smaller matrix where the row i and column are removed from this matrix
        :param i: The index of the row to delete
        :param j: The index of the column to delete
        :return: The determinant of the minor matrix
        """
        m = copy.copy(self)
        m.__delete_row(i)
        m.__delete_column(j)
        return m.determinant()

    def __cofactor(self, row, column):
        """
        Calculates the cofactor value of this matrix for the position given by row and column
        :return: The value of the calculated cofactor
        """
        if not self.__is_square():
            raise ValueError("square matrix required")
        return ((-1) ** (row + column)) * self.__minor(row, column)

    def __cofactor_matrix(self):
        """
        Calculates the cofactor matrix of this matrix
        :return: The cofactor matrix
        """
        return Matrix([[self.__cofactor(i, j) for j in range(self.columns)] for i in range(self.rows)])

    def get_column(self, column):
        """
        Retrieves the column of this matrix for the specified column index
        :param column: The column index
        :return: A list containing the elements of the row
        """
        return [row[column] for row in self.matrix]

    def get_multiple_rows(self, *rows):
        """
        Retrieves multiple rows of this matrix for the specified row indexes
        :param rows: A list of rows indexes to retrieve
        :return: A list of the wanted rows
        """
        non_repeated_rows = list(OrderedDict.fromkeys(rows))
        return [self.matrix[row] for row in non_repeated_rows]

    def get_multiple_columns(self, *columns):
        """
        Retrieves multiple columns of this matrix for the specified column indexes
        :param columns: A list of columns indexes to retrieve
        :return: A list of the wanted columns
        """
        non_repeated_columns = list(OrderedDict.fromkeys(columns))
        return [self.get_column(column) for column in non_repeated_columns]

    def scalar_mul(self, scalar):
        """
        Multiplies this matrix with the given scalar
        :param scalar: The scalar
        :return: A new Matrix with its values equal to his matrix multiplied with the scalar
        """
        return Matrix([[self.matrix[i][j] * scalar for j in range(self.columns)] for i in range(self.rows)])

    def transpose(self):
        """
        Generates a new Matrix equals to the transpose of this matrix
        :return: A new Matrix equals to the transpose of this matrix
        """
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
        """
        Calculates the adjucate of this matrix
        :return: A new matrix equals to the adjucate of this matrix
        """
        return self.__cofactor_matrix().transpose()

    def inverse(self):
        """
        Calculates the inverse of this matrix
        :return: A new matrix equals to the inverse of this matrix
        :return:
        """
        if self.determinant() == 0:
            raise ValueError('Matrix is not invertible')
        return self.adjugate().scalar_mul(1 / self.determinant())

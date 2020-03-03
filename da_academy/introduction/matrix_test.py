import copy
from matrix import Matrix

class TestMatrix:

    matrix1 = Matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    matrix11 = Matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5]])

    matrix2 = Matrix([[4, 4, 4], [-2, -3, -4], [-3, -4, -5]])

    matrix3 = Matrix([[1], [2], [3]])
    matrix4 = Matrix([[1, 2, 3]])

    def test_eq(self):
        assert self.matrix1 == self.matrix11
        assert self.matrix1 != self.matrix2

    def test_copy(self):
        assert copy.copy(self.matrix1) == self.matrix1

    def test_add(self):
        expected = Matrix([[5, 6, 7], [0, 0, 0], [0, 0, 0]])
        assert expected == self.matrix1 + self.matrix2

    def test_mul(self):
        expected = Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9]])
        assert expected == self.matrix3 * self.matrix4

        expected = Matrix([[14]])
        assert expected == self.matrix4 * self.matrix3

    def test_scalar_mul(self):
        expected = Matrix([[3, 6, 9]])
        assert self.matrix4.scalar_mul(3) == expected

        expected = Matrix([[3], [6], [9]])
        assert self.matrix3.scalar_mul(3) == expected

    def test_transpose(self):
        expected = Matrix([[1, 2, 3]])
        assert self.matrix3.transpose() == expected
        assert self.matrix3 == self.matrix3.transpose().transpose()

    def test_determinant(self):
        matrix = Matrix([[4, 1], [2, 3]])
        assert matrix.determinant() == 10

        matrix = Matrix([[-2, 3, -1], [5, -1, 4], [4, -8, 2]])
        assert matrix.determinant() == -6

    def test_adjugate(self):
        matrix = Matrix([[5, -2, 2, 7], [1, 0, 0, 3], [-3, 1, 5, 0], [3, -1, -9, 4]])
        assert matrix.adjugate() == Matrix([[-12, 76, -60, -36], [-56, 208, -82, -58], [4, 4, -2, -10], [4, 4, 20, 12]])

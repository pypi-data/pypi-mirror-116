#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (C) 2021 Fares Ahmed
#
# This file is part of matrix-py.
#
# matrix-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# matrix-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with matrix-py.  If not, see <http://www.gnu.org/licenses/>.

"""Hackable Matrix module written in pure Python + CLI

https://github.com/faresahemdb/matrix-py

Please refer to the link above for more information
on how to use the module.

You can call the CLI help with:
$ python -m matrixpy --help
"""

# pylint: disable=C0103

import random
from typing import Union, List, Tuple, NoReturn, Iterator


__all__ = ["Matrix", "MatrixError"]
__version__ = "1.0.0"
__author__ = "Fares Ahmed <faresahmed@zohomail.com>"
__dir__ = lambda: __all__


class MatrixError(Exception):
    """Error for the Matrix Object invalid operations"""


class Matrix(object):
    """Matrix Object that support Addition, Substraction, [...]"""

    def __init__(self, matrix):
        # type: (Union[List[List[int]], int, str]) -> None

        """
        Example:
            Matrix([[1, 2, 3], [4, 5, 6]])
            Matrix(3)
            Matrix("1 2 3; 4 5 6")
        """

        self.matrix = matrix  # type: List[List[int]]

        if isinstance(matrix, int):
            self.matrix = Matrix.identity(matrix).matrix

        elif isinstance(matrix, str):
            self.matrix = [
                [int(c) for c in b] for b in [a.split() for a in matrix.split(";")]
            ]

        self.rowsnum = len(self.matrix)  # type: int
        self.colsnum = len(self.matrix[0])  # type: int

        for row in self.matrix:
            if len(row) != self.colsnum:
                raise ValueError(
                    "Row `%s` has a different size" " from other rows" % row
                )

    def __repr__(self):
        # type: () -> str

        return (
            "'"
            + "; ".join([" ".join(l) for l in [list(map(str, i)) for i in self.matrix]])
            + "'"
        )

    def __str__(self):
        # type: () -> str

        mat_str = [[str(c) for c in b] for b in self.matrix]
        max_num = max([len(max(l, key=len)) for l in mat_str])
        lines = [" ".join(i) for i in [list(map(lambda i: "{:<{}}".format(i, max_num), i)) for i in mat_str]]
        return "%s\n%s" % ("\n".join(lines), "{:^{}}".format("(%sx%s)" % (self.rowsnum, self.colsnum), len(max(lines, key=len))))

    def __getitem__(self, rowcol):
        # type: (Union[int, Tuple, slice]) -> Union[Matrix, int]

        """
        Example:
            Matrix = Matrix("1 2 3; 4 5 6")
            [Row] Matrix[1, None] -> '4 5 6'  # None can be omitted
            [Col] Matrix[None, 1] -> '2; 5'
            [Item] Matrix[1, 2] -> 6
            [Slice] Matrix[0:None:1] -> "1 2 3; 4 5 6"
        """

        if isinstance(rowcol, int):
            rowcol = (rowcol, None)

        if isinstance(rowcol, tuple):
            if rowcol[1] is None:
                return Matrix([self.matrix[rowcol[0]]])
            if rowcol[0] is None:
                return Matrix([[row[rowcol[1]]] for row in self.matrix])
            return self.matrix[rowcol[0]][rowcol[1]]

        if isinstance(rowcol, slice):
            return Matrix(self.matrix[rowcol])

    def __contains__(self, other):
        # type: (Union[Matrix, int]) -> bool

        if isinstance(other, Matrix):
            for row in other.matrix:
                if row in self.matrix:
                    return True
            return False

        if isinstance(other, int):
            for row in self.matrix:
                if other in row:
                    return True
            return False

        raise NotImplementedError

    def __iter__(self):
        # type: () -> Iterator[int]

        """
        Example:
            [All Items] for item in Matrix(3)
            [Specific Row] for item in Matrix(3)[0]
            [Specific Col] for item in Matrix(3)[None, 0]
        """

        for row in self.matrix:
            for col in row:
                yield col

    def __pos__(self):
        # type: () -> Matrix

        return Matrix(self.matrix)

    def __neg__(self):
        # type: () -> Matrix

        return Matrix([[-x for x in y] for y in self.matrix])

    def __add__(self, other):
        # type: (Union[Matrix, any]) -> Matrix

        if isinstance(other, Matrix):
            if self.rowsnum != other.rowsnum or self.colsnum != other.colsnum:
                raise MatrixError(
                    "Matrices addition requires them to have the same dimensions"
                )

            return Matrix(
                [
                    [x + y for x, y in zip(m, j)]
                    for m, j in zip(self.matrix, other.matrix)
                ]
            )

        return Matrix([list(map(lambda x: x + other, x)) for x in self.matrix])

    def __sub__(self, other):
        # type: (Union[Matrix, any]) -> Matrix

        if isinstance(other, Matrix):
            if self.rowsnum != other.rowsnum or self.colsnum != other.colsnum:
                raise MatrixError(
                    "Matrices subtraction requires them to have the same dimensions"
                )

            return Matrix(
                [
                    [x - y for x, y in zip(m, j)]
                    for m, j in zip(self.matrix, other.matrix)
                ]
            )

        return Matrix([list(map(lambda x: x - other, x)) for x in self.matrix])

    def __mul__(self, other):
        # type: (Union[Matrix, any]) -> Matrix
        if isinstance(other, Matrix):
            # Since the library supports Py2.7+ Matrix Mul will
            # Work just fine if `other` is a Matrix
            return self.__matmul__(other)

        return Matrix([list(map(lambda x: x - other, x)) for x in self.matrix])

    def __matmul__(self, other):
        # type: (Union[Matrix, any]) -> Matrix

        # For the @ (Matrix Mul) operator introduced in Py3.5

        if self.colsnum != other.rowsnum:
            raise MatrixError(
                "The number of Columns in {!r} must be equal to the"
                "number of Rows in {!r}".format(self, other)
            )

        # References:
        # https://www.geeksforgeeks.org/python-program-multiply-two-matrices
        return Matrix([
            [
                sum(a * b for a, b in zip(a_row, b_col))
                for b_col in zip(*other.matrix)
            ]
            for a_row in self.matrix
        ])

    def insert_row(self, index, row):
        # type: (int, List[int]) -> NoReturn

        self.matrix.insert(index, row)
        self.__init__(self.matrix)

    def insert_col(self, index, col):
        # type: (int, List[int]) -> NoReturn

        for i in range(self.rowsnum):
            self.matrix[i].insert(index, col[i])

        self.__init__(self.matrix)

    def pop_row(self, index):
        # type: (int) -> List[int]

        popped = self.matrix.pop(index)
        self.__init__(self.matrix)
        return popped

    def pop_col(self, index):
        # type: (int) -> List[int]

        popped = []

        for i in range(self.rowsnum):
            popped.append(self.matrix[i].pop(index))

        self.__init__(self.matrix)
        return popped

    def list(self):
        # type: () -> list[List[int]]

        return self.matrix

    def transpose(self):
        # type: () -> Matrix

        """Swith the row and column indices of the Matrix

        Returns:
            Matrix: Swith the row and column indices of the Matrix
            take a look at:
            https://www.wikiwand.com/en/Transpose

        Example:
            >>> MatA = Matrix("1 2; 3 4; 5 6")
            >>> print(MatA.transpose())
            1 2 3
            4 5 6
            (2x3)
        """

        return Matrix([list(i) for i in zip(*self.matrix)])

    def diagonal(self):
        # type: () -> Matrix

        """Get the diagonal of the matrix"""

        return Matrix([[self[i, i] for i in range(self.rowsnum)]])

    # The following function (rank) is copyrighted by absognety:
    # https://github.com/absognety/Competitive-Coding-Platforms/
    # Licensed under The GPLv3 License
    def rank(self):
        # type: () -> int

        """Return the rank of the Matrix

        Returns:
            int: The rank of the Matrix
        """

        rank = self.rowsnum
        mat = self.matrix

        for row in range(rank):
            if mat[row][row]:
                for col in range(self.colsnum):
                    if col != row:
                        multiplier = mat[col][row] / mat[row][row]
                        for i in range(rank):
                            mat[col][i] -= multiplier * mat[row][i]
            else:
                reduce = True
                for i in range(row + 1, self.colsnum):
                    if mat[i][row]:
                        for s in range(rank):
                            temp = mat[row][s]
                            mat[row][s] = mat[i][s]
                            mat[i][s] = temp
                        reduce = False
                        break
                if reduce:
                    rank -= 1
                    for i in range(self.colsnum):
                        mat[i][row] = mat[i][rank]
                row -= 1

        return rank

    def is_square(self):
        # type: () -> bool

        """Return True if the Matrix is square

        Returns:
            bool: True if the given Matrix (self)
            is square (rows number == columns number).
            else returns False
        """

        return self.rowsnum == self.colsnum

    def is_symmetric(self):
        # type: () -> bool

        """Return True if the Matrix is symmetric

        Raises:
            MatrixError: if the given Matrix is not
            square Matrix. Explaination:
            https://www.wikiwand.com/en/Symmetric_matrix

        Returns:
            bool: True if the given Matrix (self)
            is symmetric (Matrix == Matrix transpose).
            else returns False
        """

        if not self.is_square():
            raise MatrixError("symmetric matrix is a square matrix")

        if self.matrix == self.transpose().tolist():
            return True

        return False

    @staticmethod
    def identity(size):
        # type: (int) -> Matrix

        """Return a new I (sizeXsize) Matrix

        Args:
            size (int): size=2 -> (2x2) Matrix

        Returns:
            Matrix: New I Matrix (All the diagonal
            items == 1)

        Example:
            print(Matrix.identity(3)) # 3 -> (3x3) Matrix
            Output: 1 0 0
                    0 1 0
                    0 0 1
                    (3x3)
        """

        result = [[0] * 3 for _ in range(size)]

        for i in range(size):
            result[i][i] = 1

        return Matrix(result)

    @staticmethod
    def zero(size):
        # type: (int) -> Matrix

        """Return a new zero (sizeXsize) Matrix

        Args:
            size (int): size=2 -> (2x2) Matrix

        Returns:
            Matrix: New zero Matrix (all matrix
            items == 0)

        Example:
            print(Matrix.zero(3)) # 2 -> (2x2) Matrix
            Output: 0 0 0
                    0 0 0
                    (3x3)
        """

        return Matrix([[0] * size] * size)

    @staticmethod
    def random(size, a, b):
        # type: (Tuple, int, int) -> Matrix

        """Return (size) Matrix with random integers in range (a, b)

        Args:
            size (tuple): (3,3) -> (3x3) Matrix
            a, b (int), (int): in the range a:b

        Returns:
            Matrix: (size) Matrix with random
            integer in the range a:b
        """

        return Matrix(
            [[random.randint(a, b) for _ in range(size[1])] for _ in range(size[0])]
        )


def main(args=None):
    # type: (None) -> None

    from textwrap import dedent
    from typing import Text
    from operator import add, sub, mul
    import sys

    def error(s, t):
        # type: (Text, Text) -> NoReturn
        sys.exit(
            (
                "{red}{bold}ERROR: {reset}{red}{}.{reset}\n" +
                "{blue}{bold}TIP: {reset}{blue}{}{reset}"
            ).format(
                s,
                "... '1 2 3; 4 5 6'"
                if t == "Matrix"
                else "... 10"
                if t == "int"
                else "3x3"
                if t == "Matrix_size"
                else "... +, -, *"
                if t == "operator"
                else t,
                **colors
            )
        )

    def matrix_exit(m):
        # type: (Matrix) -> NoReturn
        m = str(m)  # type: str
        sys.exit(
            "{green}{}\n{blue}{}{reset}".format(
                m[: m.rfind("\n")], m.splitlines()[-1], **colors
            )
        )

    args = list(map(lambda s: s.strip("-").lower(), sys.argv[1:]))  # type: List[str]

    try:
        args.pop(args.index("no-colors"))
        allow_colors = False
    except ValueError:
        allow_colors = True

    colors = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "bold": "\x1b[1m",
        "reset": "\x1b[0m",
    }

    colors = {k: allow_colors * v for k, v in colors.items()}

    if not args:
        args.append("help")

    args_one_char = [a[0] for a in args]

    if "h" in args_one_char:
        sys.exit(dedent(
            """
            Welcome to matrixpy Command-Line Interface program!

            {yellow}{bold}┍————————————————————————————- /ᐠ｡ꞈ｡ᐟ\ ————————————————————————————┑{reset}

            {yellow}Mathmatical Operations{reset}:
            {green}    Addition (+){reset}        matrixpy "1 2 3; 4 5 6" "+" "1 2 3; 4 5 6"
            {green}    Substraction (-){reset}    matrixpy "1 2 3; 4 5 6" "-" "1 2 3; 4 5 6"
            {green}    Multiplication (*){reset}  matrixpy "1 2 3; 4 5 6" "*" "1 2; 3 4; 5 6"

            {yellow}Commands{reset}:
            {green}    Transpose, -t{reset}       Get the transpose of a Matrix 
                                    Example: matrixpy transpose "1 2 3; 4 5 6"

            {green}    Randint, -r{reset}         Get a random Matrix in a specific range 
                                    Example: matrixpy randint 1 100 3x3

            {yellow}Other{reset}:
            {green}    Help, -h{reset}            Get help about the CLI usage
            {green}    Version, -v{reset}         Get the version of the matrixpy

            {yellow}{bold}┕————————————————————————————(..)(..) ∫∫——————————————————————————-┙{reset}
            """.format(**colors)
        ))

    if "v" in args_one_char:
        sys.exit(
            "{yellow}Version{reset} {green}{}{reset}".format(__version__, **colors)
        )

    def get_matrix(name, index):
        # type: (str, int) -> Matrix
        if len(args) == index:
            error("No %s has been defined" % name, "Matrix")
        try:
            return Matrix(args[index])
        except (ValueError, TypeError):
            error("Define %s correctly" % name, "Matrix")

    if args_one_char[0] == "t":
        matrix_exit(get_matrix("Matrix", 1).transpose())

    if args[0].startswith("rand"):

        def get_num(name, index):
            # type: (str, int) -> int
            if len(args) == index:
                error("No %s has been defined" % name, "int")
            try:
                return int(args[index])
            except ValueError:
                error("%s Should be numeric" % name, "int")

        a = get_num("A", 1)
        b = get_num("B", 2)

        if len(args) == 3:
            error("No Matrix Size has been defined", "Matrix_size")

        try:
            size = tuple(map(int, args[3].split("x")))
        except ValueError:
            size = (0,)

        if len(size) != 2:
            error("Define the Matrix Size correctly", "Matrix_size")

        matrix_exit(Matrix.random(size, a, b))

    if args[0] == "rank":
        sys.exit(
            "{yellow}Rank{reset}: {green}{}{reset}".format(
                get_matrix("Matrix", 1).rank(), **colors
            )
        )

    def get_op(index):
        # type: (int) -> str
        if len(args) == index:
            error("No operator has been defined.", "operator")
        op = args[index]
        if op not in ["+", "-", "*"]:
            error("{!r} is not a valid operator.".format(op), "operator")
        return op

    mat_a = get_matrix("MatA", 0)
    op = get_op(1)
    mat_b = get_matrix("MatB", 2)

    try:
        result = (
            add(mat_a, mat_b)
            if op == "+"
            else sub(mat_a, mat_b)
            if op == "-"
            else mul(mat_a, mat_b)
        )
    except MatrixError as e:
        error(e, "Null")

    matrix_exit(result)


if __name__ == "__main__":
    main()

from typing import Iterable, Self


class Matrix[T]:
    def __init__(self, data: Iterable[Iterable[T]]):
        self.data = list(list(row) for row in data)
        self.size = (len(self.data), len(self.data[0]))
        
        assert \
            all(len(self.data[0]) == len(row) for row in self.data), \
            "Not all row lenghts are equal."

    def __neg__(self):
        return  self.per_element(lambda ele: -ele)

    def __add__(self, other: Self):
        assert self.size == other.size, "Sizes are not equal."
        return Matrix(
            (ele1 + ele2 for ele1, ele2 in zip(row1, row2))
            for row1, row2 in zip(self.data, other.data)
        )
    
    def __sub__(self, other: Self):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.per_element(lambda ele: other * ele)
        elif isinstance(other, Matrix):
            return self.__matrix_mul(other)
        raise TypeError("Rhs type neither scalar (real number), nor matrix.")

    def per_element(self, func, *args):
        return Matrix(
            (func(ele, *args) for ele in row) for row in self.data
        )

    def __matrix_mul(self, other: Self):
        assert \
            self.size[1] == other.size[0], \
            "Number of columns in lhs is not " \
            "equal to number of rows in rhs."

        data = [[None] * other.size[1] for _ in range(self.size[0])]
        m = self.size[0]
        n = self.size[1]
        p = other.size[1]

        for i in range(m):
            for j in range(p):
                data[i][j] = sum(
                    self[i][r] * other[r][j] for r in range(n)
                )
        
        return Matrix(data)

    def transpose(self) -> Self:
        return Matrix(zip(*self.data))

    def __getitem__(self, row_idx: int) -> list[T]:
        return self.data[row_idx]

    def __eq__(self, other: Self):
        return self.data == other.data

    def __ne__(self, other: Self):
        return self.data != other.data

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.data))

    __rmul__ = __mul__


class Vector[T](Matrix):
    def __init__(self, data: Iterable[T]):
        super().__init__(map(lambda ele: (ele,), data)) 

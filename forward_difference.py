from prettytable import PrettyTable
from interpolation import Interpolation
from polynomial import Polynomial


class ForwardDifference(Interpolation):
    def __init__(self, points: list[(float, float)]):
        super().__init__(points)
        self.__ni: list[Polynomial] = [Polynomial([1])] * self._n
        self.__calculate_ni()
        self._p = Polynomial([0])
        self.__calculate_p()
        self.__print()

    def __calculate_nfi(self, n: int, i: int):
        if n == 0:
            return self._points[i][1]
        else:
            return self.__calculate_nfi(n - 1, i + 1) - self.__calculate_nfi(n - 1, i)

    def __calculate_ni(self):
        t, _ = Polynomial([1, -self._points[0][0]]).quotient(self._points[1][0] - self._points[0][0])
        for i in range(1, self._n):
            self.__ni[i], _ = self.__ni[i - 1].product(t.subtraction(i - 1)).quotient(i)

    def __calculate_p(self):
        ai: list[float] = [0] * self._n
        for i in range(self._n):
            ai[i] = self.__calculate_nfi(i, 0)
        for i, val in enumerate(self.__ni):
            self._s.append(ai[i])
            self._s.append(val)
            self._p = self._p.sum(val.product(ai[i]))

    def __print(self):
        print("================================")
        print("Forward Difference")
        print("d^nfi = d^(n - 1)f(i + 1) - d^(n - 1)fi")
        table = PrettyTable()
        for n in range(self._n):
            col = []
            for i in range(n):
                col.append("")
            for i in range(self._n - n):
                col.append(self.__calculate_nfi(n, i))
                col.append("")
            for i in range(n):
                col.append("")
            col.pop()
            header = ""
            if n == 0:
                header = ""
            elif n == 1:
                header = "d"
            else:
                header = f"d^{n}"
            header += "fi"
            table.add_column(header, col, align='c')
        print(table)
        self._print()
        print("================================")

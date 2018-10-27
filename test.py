from typing import Sequence, List, TypeVar


class BaseClass:
    def __init__(self, data=None, *args, **kwargs):
        super().__init__()
        self.CanCalculate = True
        if data is None:
            data = []
            self.CanCalculate = False
        self._mydata = list(data)
        self.multiplier = 1

    @property
    def data(self):
        return self._mydata


class ChildClass(BaseClass):
    def sum_mul_data(self):
        return self.multiplier * sum(self.data)


class SecondChildClass(BaseClass):
    def sum_div_data(self):
        return sum(self.data) / self.multiplier


T = TypeVar("T", bound=BaseClass)


def myFun(input: Sequence[T]) -> List[T]:
    out = []
    for n, i in enumerate(input):
        if i.CanCalculate:
            i.multiplier = 10**n
            out.append(i)
    return out


childs = [ChildClass([1,2,3,4]), ChildClass(), ChildClass([1,2,3,4])]

t = myFun(childs)
for idx in t:
    print(idx.sum_mul_data())


childs = [SecondChildClass([1,2,3,4]), SecondChildClass(), SecondChildClass([1,2,3,4])]

t = myFun(childs)
for idx in t:
    print(idx.sum_div_data())

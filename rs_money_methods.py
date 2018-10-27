from typing import Iterable, Tuple
import itertools
import functools
import rs_item


class RSMethod:
    def __init__(self,
                 name=None,
                 input_seq: Iterable[Tuple[rs_item.RSItem, float]]=None,
                 output_seq: Iterable[Tuple[rs_item.RSItem, float]]=None,
                 num_per_hour: float=None,
                 hourly_input_seq: Iterable[Tuple[rs_item.RSItem, float]] = None,
                 hourly_output_seq: Iterable[Tuple[rs_item.RSItem, float]] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        if name is None:
            raise TypeError("__init__() missing 1 required positional argument: 'name'")
        if num_per_hour is None:
            raise TypeError("__init__() missing 1 required positional argument: 'num_per_hour'")
        self.name = name
        if input_seq is None:
            input_seq = []
        if output_seq is None:
            output_seq = []
        self._input_list = list(input_seq)
        self._output_list = list(output_seq)

        if hourly_input_seq is not None:
            for item, num in hourly_input_seq:
                self._input_list.append((item, num/num_per_hour))
        if hourly_output_seq is not None:
            for item, num in hourly_output_seq:
                self._output_list.append((item, num/num_per_hour))
        self.rate = num_per_hour

    @property
    def input_price(self) -> float:
        return sum(i.current_price * n for i, n in self.input_list)

    @property
    def output_price(self) -> float:
        return sum(i.current_price * n for i, n in self.output_list)

    @property
    def profit_per_item(self) -> float:
        return self.output_price - self.input_price

    @property
    def profit_per_hour(self) -> float:
        return self.profit_per_item * self.rate

    @property
    def input_list(self):
        return self._input_list

    @property
    def output_list(self):
        return self._output_list

    def __str__(self):
        input_str = "    Input: " + "\n           ".join(("{0} {1} ({2})".format(num, item, num * item.current_price)
                                                          for item, num in self.input_list))
        output_str = "    Output: " + "\n            ".join(("{0} {1} ({2})".format(num, item, num * item.current_price)
                                                             for item, num in self.output_list))
        profit_str = "    Profit: {0} gp, {1} gp/hr".format(self.profit_per_item, self.profit_per_hour)
        s = "\n".join((self.name, input_str, output_str, profit_str))
        return s


class RSLazyMethod(RSMethod):
    def __init__(self,
                 input_seq: Iterable[Tuple[rs_item.RSItem, float]]=None,
                 output_seq: Iterable[Tuple[rs_item.RSItem, float]]=None,
                 num_per_hour: float=None,
                 hourly_input_seq: Iterable[Tuple[rs_item.RSItem, float]] = None,
                 hourly_output_seq: Iterable[Tuple[rs_item.RSItem, float]] = None,
                 *args, **kwargs):
        super().__init__(num_per_hour=num_per_hour, *args, **kwargs)
        if input_seq is None:
            input_seq = []
        if output_seq is None:
            output_seq = []
        self._input_list = input_seq
        self._output_list = output_seq

        self._hourly_input_list = []
        if hourly_input_seq is not None:
            self._hourly_input_list = ((item, num/num_per_hour) for item, num in hourly_input_seq)
        self._hourly_output_list = []
        if hourly_output_seq is not None:
            self._hourly_output_list = ((item, num/num_per_hour) for item, num in hourly_output_seq)

        self._input_list = itertools.chain(self._input_list, self._hourly_input_list)
        self._output_list = itertools.chain(self._output_list, self._hourly_output_list)

    @property
    @functools.lru_cache()
    def input_list(self):
        return list(self._input_list)

    @property
    @functools.lru_cache()
    def output_list(self):
        return list(self._output_list)

    # noinspection PyStatementEffect
    def load(self):
        self.input_list
        self.output_list
        return


class RSMoneyMethod(RSMethod):
    pass

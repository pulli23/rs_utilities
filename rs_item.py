from typing import Union
import re


def num_str_to_value(numstr: Union[int, str]) -> float:
    special_symbols = {
        "k": 1000,
        "m": 1000000,
        "b": 1000000000,
        "t": 1000000000000
    }
    try:
        return float(numstr)
    except ValueError:
        numstr = numstr.lower()
        numstr = numstr.replace(",", "")
        pattern = "(.+?)([{0}]|$)".format("".join(special_symbols.keys()))
        match_objects = re.finditer(pattern, numstr)
        v = sum(float(mo.group(1)) * special_symbols.get(mo.group(2), 1) for mo in match_objects)
        return v


class RSItem:
    def __init__(self, item_json: dict):
        self.full_json = item_json
        self.name = item_json["name"]
        self.idx = int(item_json["id"])
        self.desc = item_json["description"]
        t_price = item_json["current"]["price"]
        self.current_price = num_str_to_value(t_price)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{cls}(name={name}, id={idx})".format(cls=self.__class__.__name__, name=self.name, idx=self.idx)


# noinspection PyMissingConstructor
class GPItem(RSItem):
    def __init__(self):
        self.full_json = ""
        self.name = "gp"
        self.idx = -1
        self.desc = "gold points"
        self.current_price = 1
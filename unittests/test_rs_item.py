import json

import pytest
import rs_item


def build_json(name: str, idx: int, description: str, price: str) -> str:
    r = '{{"name":"{0}","id":{1},"description":"{2}","current":{{"price":"{3}"}}}}' \
        .format(name, idx, description, price)
    return r


@pytest.mark.parametrize("number_str,expected", [("100", 100),
                                                 ("1k", 1000),
                                                 ("10000k",10000000),
                                                 ("1m2k3", 1002003)])
def test_num_str_to_value(number_str, expected):
    v = rs_item.num_str_to_value(number_str)
    assert v == expected


@pytest.mark.parametrize("name,idx,description,price", [("a", 1, "this is a", "100"),
                                                        ("b", 2, "this is b", "100K"),
                                                        ("c", 3194, "this is c", "10M")])
def test_rs_item_init(name, idx, description, price):
    json_str = build_json(name, idx, description, price)
    dat = json.loads(json_str)
    item = rs_item.RSItem(dat)
    assert item.name == name and item.idx == idx and item.desc == description
    assert item.current_price == rs_item.num_str_to_value(price)

import pytest
import loader
import requests


@pytest.fixture(scope="module")
def osrsge_downloader():
    return loader.DataOSRSGE()


@pytest.mark.parametrize("test_input,expected", [
        (4151, "Abyssal whip"),
        (2, "Cannonball"),
        (6, "Cannon base"),
    ])
def test_get_item(osrsge_downloader, test_input, expected):
    dat = osrsge_downloader.get_item(test_input)
    assert dat["name"] == expected
    assert dat["id"] == test_input


def test_get_item_bad(osrsge_downloader):
    with pytest.raises(requests.HTTPError):
        osrsge_downloader.get_item(-1)


@pytest.mark.parametrize("name,expected", [
    ("abyssal whip", 1),
    ("rune", 95)
])
def test_find_items(osrsge_downloader, name, expected):
    dat = osrsge_downloader.find_items(name)
    l = len(dat)
    assert l == expected


@pytest.mark.parametrize("name", [
    ("abyssal whip"), ("cosmic rune"), ("sapphire")
])
def test_find_item(osrsge_downloader, name):
    dat = osrsge_downloader.find_best_item(name)
    assert dat["name"].lower() == name.lower()
    item_id = dat["id"]
    feedback_dat = osrsge_downloader.get_item(item_id)
    assert feedback_dat["name"].lower() == name.lower()


@pytest.mark.parametrize("idx", [(2), (6), (4151)])
def test_get_rsbuddy_item(osrsge_downloader, idx):
    dat = osrsge_downloader.get_rsbuddy_item(idx)
import requests
import difflib
import json
import time
import functools
import inspect


class DataOSRSGE:
    def __init__(self):
        self.session = requests.session()
        self.base_uri = r"http://services.runescape.com/m=itemdb_oldschool/api"
        self.catalogue_uri = r"/catalogue/detail.json"
        self.search_uri = r"/catalogue/items.json"
        self.rsbuddy_uri = r"https://api.rsbuddy.com/grandExchange"

    @functools.lru_cache()
    def get_item(self, idx):
        payload = {"item": str(idx)}
        uri = self.base_uri + self.catalogue_uri
        res = self.session.get(uri, params=payload)
        res.raise_for_status()
        dat = res.json()
        return dat["item"]

    def get_rsbuddy_item(self, idx):
        pass

    @functools.lru_cache()
    def get_page_of_items(self, name: str, page: int):
        payload = {"category": "1",
                   "alpha": name,
                   "page": str(page)}
        uri = self.base_uri + self.search_uri

        res = None
        n = 0.2
        for test_runs in range(10):
            res = self.session.get(uri, params=payload)
            res.raise_for_status()
            try:
                dat = res.json()
                break
            except json.decoder.JSONDecodeError:
                print("... Server dc, reconnecting in {} seconds".format(n))
                time.sleep(n)
                n *= 2
                pass
        else:
            raise ValueError("Bad server at item: {0}, page: {1}".format(name, page))
        return dat["items"]

    @functools.lru_cache()
    def find_items(self, name: str):
        name = name.lower()
        page_num = 0
        all_items = []
        print("Searching item {}".format(name))
        while True:
            items = self.get_page_of_items(name, page_num)
            all_items.extend(items)
            if len(items) < 12:
                break
            page_num += 1
        return all_items

    def find_best_item(self, name):
        def get_relative_item(item):
            return difflib.SequenceMatcher(None, item["name"].lower(), name.lower()).ratio()

        all_items = self.find_items(name)
        try:
            return max(all_items,
                       key=lambda item: get_relative_item(item))
        except ValueError:
            raise KeyError("item '{0}' not found".format(name))

    def clear_cache(self):
        d = self.__class__.__dict__.items()
        for i, v in d:
            try:
                v.cache_clear()
            except AttributeError:
                pass

from typing import Sequence as Seq
from typing import TypeVar, Tuple, List, Any
from functools import lru_cache
from itertools import chain
import re

import math

from rs_money_methods import RSMoneyMethod, RSMethod
from rs_skill_method import RSSkillMethod, RSLazySkillMethod
from rs_item import RSItem, GPItem
import loader


def make_unfished_potion_method(db, herbname, potionname=None):
    if potionname is None:
        potionname = herbname
    m = RSSkillMethod(name='make unfinished {potionname} potion'.format(potionname=potionname),
                      input_seq=[(RSItem(db.find_best_item('vial of water')), 1),
                                 (RSItem(db.find_best_item(herbname)), 1)],
                      output_seq=[(RSItem(db.find_best_item('{potionname} potion (unf)'.format(potionname=potionname))), 1)],
                      num_per_hour=3850,
                      exp_per_item=0
                      )
    return m


def compare_bank_standing():
    db = loader.DataOSRSGE()

    methods = []
    methods.append(RSSkillMethod(name='string yew long',
                                 input_seq=[(RSItem(db.find_best_item('yew longbow (u)')), 1),
                                            (RSItem(db.find_best_item('bow string')), 1)],
                                 output_seq=[(RSItem(db.find_best_item('yew longbow')), 1)],
                                 num_per_hour=2400,
                                 exp_per_item=67.5
                                 ))
    methods.append(RSSkillMethod(name='cut yew long',
                                 input_seq=[(RSItem(db.find_best_item('yew log')), 1)],
                                 output_seq=[(RSItem(db.find_best_item('yew longbow (u)')), 1)],
                                 num_per_hour=1800,
                                 exp_per_item=67.5
                                 ))
    methods.append(RSSkillMethod(name='string magic long',
                                 input_seq=[(RSItem(db.find_best_item('magic longbow (u)')), 1),
                                            (RSItem(db.find_best_item('bow string')), 1)],
                                 output_seq=[(RSItem(db.find_best_item('magic longbow')), 1)],
                                 num_per_hour=2400,
                                 exp_per_item=83.3
                                 ))
    methods.append(RSSkillMethod(name='cut magic long',
                                 input_seq=[(RSItem(db.find_best_item('magic log')), 1)],
                                 output_seq=[(RSItem(db.find_best_item('magic longbow (u)')), 1)],
                                 num_per_hour=1800,
                                 exp_per_item=83.3
                                 ))
    methods.extend(make_unfished_potion_method(db, herbname) for herbname in [
        'marrentill', 'tarromin', 'harralander', 'avantoe','toadflax', 'kwuarm',
        'cadantine', 'snapdragon', 'lantadyme', 'dwarf weed', 'torstol',
    ])
    methods.extend(make_unfished_potion_method(db, *herbname) for herbname in [
        ('irit leaf', 'irit'), ('ranarr weed', 'ranarr'), ('guam leaf', 'guam')
    ])
    methods = [method for method in methods if method.input_price < 7000]

    methods.sort(key=lambda x: x.profit_per_hour)
    namewidth = max(len(method.name) for method in methods)
    profitwidth = max(len(str(method.profit_per_hour)) for method in methods)
    xpwidth = max(len(str(method.profit_per_hour)) for method in methods)
    print(xpwidth)
    for method in methods:
        print("{name: <{namewidth}} | {profit: >{profitwidth}} gp/hr | {xp: >{xpwidth}} xp/hr | {gpitem} gp".format(
            name=method.name,
            profit=method.profit_per_hour,
            xp=method.experience_per_hour,
            gpitem=method.profit_per_item,
            namewidth=namewidth,
            profitwidth=profitwidth,
            xpwidth=xpwidth
        ))
    print(methods[-1])

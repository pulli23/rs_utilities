import itertools

from rs_money_methods import RSMoneyMethod, RSMethod
from rs_skill_method import RSSkillMethod, RSLazySkillMethod
from rs_item import RSItem, GPItem
import loader


class Herb:
    def __init__(self, name: str, xp: float, potion_prefix: str = None, grimy_name: str = None):
        self.name = name
        self.xp = xp
        if grimy_name is None:
            grimy_name = 'grimy {herbname}'.format(herbname=name)
        if potion_prefix is None:
            potion_prefix = name
        self.grimy_name = grimy_name
        self.potion_prefix = potion_prefix

    def generate_unfinished_potion_method(self, db: loader.DataOSRSGE):
        m = RSSkillMethod(name='make unfinished {potionname} potion'.format(potionname=self.potion_prefix),
                          input_seq=[(RSItem(db.find_best_item('vial of water')), 1),
                                     (RSItem(db.find_best_item(self.name)), 1)],
                          output_seq=[
                              (RSItem(
                                  db.find_best_item('{potionname} potion (unf)'.format(potionname=self.potion_prefix))),
                               1)],
                          num_per_hour=3850,
                          exp_per_item=0)
        return m

    def generate_clean_herb_method(self, db: loader.DataOSRSGE, xp_value: float = 4):
        m = RSSkillMethod(name='clean {herbname}'.format(herbname=self.name),
                          input_seq=[(RSItem(db.find_best_item(self.grimy_name)), 1)],
                          output_seq=[
                              (RSItem(db.find_best_item(self.name)), 1),
                              (GPItem(), self.xp * xp_value)
                          ],
                          num_per_hour=6500,
                          exp_per_item=self.xp)
        return m


def make_fletch_methods(db, xp_value: float = 0):
    methods = [
        RSSkillMethod(name='string yew long',
                      input_seq=[(RSItem(db.find_best_item('yew longbow (u)')), 1),
                                 (RSItem(db.find_best_item('bow string')), 1)],
                      output_seq=[(RSItem(db.find_best_item('yew longbow')), 1)],
                      num_per_hour=2400,
                      exp_per_item=67.5),
        RSSkillMethod(name='cut yew long',
                      input_seq=[(RSItem(db.find_best_item('yew log')), 1)],
                      output_seq=[(RSItem(db.find_best_item('yew longbow (u)')), 1)],
                      num_per_hour=1800,
                      exp_per_item=67.5),
        RSSkillMethod(name='string magic long',
                      input_seq=[(RSItem(db.find_best_item('magic longbow (u)')), 1),
                                 (RSItem(db.find_best_item('bow string')), 1)],
                      output_seq=[(RSItem(db.find_best_item('magic longbow')), 1)],
                      num_per_hour=2400,
                      exp_per_item=83.3),
        RSSkillMethod(name='cut magic long',
                      input_seq=[(RSItem(db.find_best_item('magic log')), 1)],
                      output_seq=[(RSItem(db.find_best_item('magic longbow (u)')), 1)],
                      num_per_hour=1800,
                      exp_per_item=83.3),
    ]
    return methods


def make_herblore_methods(db, xp_value: float = 0):
    methods = []
    herbs = [
        Herb('guam leaf', 2.5, potion_prefix='guam'),
        Herb('marrentill', 3.75),
        Herb('tarromin', 5),
        Herb('harralander', 6.25),
        Herb('ranarr weed', 7.5, potion_prefix='ranarr'),
        Herb('toadflax', 8),
        Herb('irit leaf', 8.75, potion_prefix='irit'),
        Herb('avantoe', 10),
        Herb('kwuarm', 11.25),
        Herb('snapdragon', 11.75),
        Herb('cadantine', 12.5),
        Herb('lantadyme', 13.15),
        Herb('dwarf weed', 13.75),
        Herb('torstol', 15),
        # 'cadantine', 'lantadyme', 'dwarf weed', 'torstol',
    ]
    methods.extend(herb.generate_unfinished_potion_method(db) for herb in herbs)
    methods.extend(herb.generate_clean_herb_method(db, xp_value) for herb in herbs)

    herbname = 'cadantine'
    potionname = 'cadantine'
    methods.append(
        RSSkillMethod(name='make unfinished {potionname} blood potion'.format(potionname=potionname),
                      input_seq=[(RSItem(db.find_best_item('vial of blood')), 1),
                                 (RSItem(db.find_best_item(herbname)), 1)],
                      output_seq=[
                          (RSItem(db.find_best_item('{potionname} blood potion (unf)'.format(potionname=potionname))),
                           1)],
                      num_per_hour=3850,
                      exp_per_item=0)
    )
    return methods


def make_magic_methods(db, xp_value: float = 0):
    r = range(18, 28)
    full_range = range(18, 39)
    num_glass = sum(r) + (r[-1] * (len(full_range) - len(r)) if len(full_range) > len(r) else 0)
    average_glass = num_glass / (max(len(full_range), len(r)))
    methods = [
        RSSkillMethod(name='string flax spell',
                      input_seq=[(RSItem(db.find_best_item('nature rune')), 2),
                                 (RSItem(db.find_best_item('astral rune')), 1),
                                 (RSItem(db.find_best_item('flax')), 5)],
                      output_seq=[(RSItem(db.find_best_item('bow string')), 5), (GPItem(), 75 * xp_value)],
                      num_per_hour=1130,
                      exp_per_item=75),
        RSSkillMethod(name='Superglass make',
                      input_seq=[(RSItem(db.find_best_item('astral rune')), 2),
                                 (RSItem(db.find_best_item('seaweed')), 13),
                                 (RSItem(db.find_best_item('bucket of sand')), 13)],
                      output_seq=[(RSItem(db.find_best_item('molten glass')), 13 * 1.3), (GPItem(), 130 * xp_value)],
                      num_per_hour=685,
                      exp_per_item=130),
        RSSkillMethod(name='Superglass make (giant seaweed)',
                      input_seq=[(RSItem(db.find_best_item('astral rune')), 2),
                                 (RSItem(db.find_best_item('giant seaweed')), 3),
                                 (RSItem(db.find_best_item('bucket of sand')), 18)],
                      output_seq=[(RSItem(db.find_best_item('molten glass')), average_glass),
                                  (GPItem(), 180 * xp_value)],
                      num_per_hour=685,
                      exp_per_item=180),
    ]
    return methods


def compare_bank_standing(method_funcs=None):
    db = loader.DataOSRSGE()

    if method_funcs is None:
        method_funcs = [make_fletch_methods, make_herblore_methods, make_magic_methods]

    methods = []
    d = itertools.chain.from_iterable(f(db) for f in method_funcs)
    methods.extend(d)

    methods = [method for method in methods if method.profit_per_item / method.input_price > 0.02]

    methods.sort(key=lambda x: x.profit_per_hour)
    if len(methods) == 0:
        print('No methods fullfill criteria')
        return
    namewidth = max(len(method.name) for method in methods)
    profitwidth = max(len(str(f'{method.profit_per_hour:.0f}')) for method in methods)
    xpwidth = max(len(str(f'{method.experience_per_hour:.0f}')) for method in methods)
    gpitemwidth = max(len(str(f'{method.profit_per_item:.1f}')) for method in methods)
    for method in methods:
        print(
            "{method.name:<{namewidth}} | "
            "{method.profit_per_hour:>{profitwidth}.0f} gp/hr | "
            "{method.experience_per_hour:>{xpwidth}.0f} xp/hr | "
            "{method.profit_per_item:>{gpitemwidth}.1f} gp | "
            "{relprofit: .4f}"
            .format(
                method=method,
                namewidth=namewidth,
                profitwidth=profitwidth,
                xpwidth=xpwidth,
                gpitemwidth=gpitemwidth,
                relprofit=method.profit_per_item / method.input_price
            )
        )
    print(methods[-1])


if __name__ == '__main__':
    compare_bank_standing()

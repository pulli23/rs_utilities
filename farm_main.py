from typing import Sequence as Seq
from typing import TypeVar, Tuple, List, Any
from functools import lru_cache
from itertools import chain
import math
import re

from rs_money_methods import RSMoneyMethod, RSMethod
from rs_skill_method import RSFarmingMethod, RSSkillMethod, RSFarmingLazyMethod
from rs_item import RSItem, GPItem
import loader


class FarmData:
    @property
    def input_data(self):
        return ((RSItem(self.db.find_best_item(name)), amount)
                for name, amount in self._input_names)

    @property
    def output_data(self):
        return ((RSItem(self.db.find_best_item(name)), amount)
                for name, amount in self._output_names)

    @property
    def payment_data(self):
        return ((RSItem(self.db.find_best_item(name)), amount)
                for name, amount in self._payment_names)

    def __init__(self, db: loader.DataOSRSGE, name: str, plant_xp: float, check_xp: float, harvest_xp: float,
                 inputs: Seq[Tuple[str, float]] = None, payments: Seq[Tuple[str, float]] = None,
                 outputs: Seq[Tuple[str, float]] = None, harvest_amount: int = None,
                 time_walk_farm: float = 120, time_harvest: float = 20, steps: int = 4, can_protect=True,
                 base_disease: float = None):
        if inputs is None:
            inputs = []
        if payments is None:
            payments = []
        if outputs is None:
            outputs = []
        self.db = db
        self.name = name
        self._input_names = inputs  # type: Seq[Tuple[str, float]]
        self._payment_names = payments  # type: Seq[Tuple[str, float]]
        self._output_names = outputs  # type: Seq[Tuple[str, float]]
        self.plant_xp = plant_xp
        self.harvest_xp = harvest_xp
        self.check_xp = check_xp
        if harvest_amount is None:
            try:
                harvest_amount = outputs[0][1]
            except IndexError:
                harvest_amount = 0
        self.harvest_amount = harvest_amount
        self._input_data = None
        self._pay_data = None
        self._output_data = None
        self.time_walk_farm = time_walk_farm
        self.time_harvest = time_harvest
        self.steps = steps
        self.can_protect = can_protect
        self.base_disease = base_disease

    def clone(self):
        return FarmData(self.db, self.name, self.plant_xp, self.check_xp, self.harvest_xp,
                        self._input_names, self._payment_names, self._output_names,
                        self.harvest_amount, self.time_walk_farm, self.time_harvest, self.steps,
                        self.can_protect, self.base_disease)


def compare_all_tree_farming(name_pattern: str = None, bottomless_bucket: bool = False):
    db = loader.DataOSRSGE()
    composts = ((RSItem(db.find_best_item("supercompost")), 1/8),
                (RSItem(db.find_best_item("ultracompost")), 1/10))
    for c in composts:
        print(c[0], c[0].current_price)

    allfarmmethods = []
    allfarmmethods.extend(build_fruit_tree_list(db))
    l1 = build_tree_list(db)
    allfarmmethods.extend(l1)
    l3 = build_hardwood_list(db)
    allfarmmethods.extend(l3)
    l2 = build_other_farm_list(db)
    allfarmmethods.extend(l2)
    build_methods = []
    for method in allfarmmethods:
        l = list(build_farm_methods(composts, method, bottomless_bucket))
        build_methods.extend(l)
        compare_methods(l)
        print("--------------")

    print("--------------")
    if name_pattern:
        methods = find_methods_by_name(build_methods, name_pattern)
        for m in methods:
            print(m)

    return allfarmmethods


def find_methods_by_name(methodlist: Seq[RSMethod], name_pattern) -> List[Any]:
    out = []
    for i in methodlist:
        if re.search(name_pattern, i.name) is not None:
            out.append(i)
    return out


def compare_methods(methods: List[RSSkillMethod]):
    methods.sort(key=lambda x: x.gp_per_xp, reverse=True)
    strlen = max(len(x.name) for x in methods)
    max_experience_per_hour = 0
    for method in methods:
        if method.experience_per_hour > max_experience_per_hour:
            max_experience_per_hour = method.experience_per_hour
            print('{:<{length}} | {gp_per_xp:.3} | {xp}'.format(method.name, length=strlen,
                                                                gp_per_xp=method.gp_per_xp,
                                                                xp=method.experience_per_hour))


def calculate_success_rate(base_disease: float, steps: float, compost_modifier: float,
                           do_resurrect: bool = False, resurrect_chance: float = 0.75) -> float:
    modified_rate = compost_modifier * base_disease
    base_success = math.pow(1-modified_rate, steps)
    if not do_resurrect:
        return base_success
    fail_chance = 1 - base_success
    # resurrection success is the chance, combined with the chance it is not already resurrected previous round
    modified_fail = fail_chance * ((1 - resurrect_chance) + resurrect_chance * fail_chance * 0.5)
    modified_success = 1 - modified_fail
    return modified_success


def _build_single_output_type_farm_methods(data: FarmData, compost: RSItem, compost_rate: float,
                                           bottomless_bucket: bool = False, cut_payment: int = 200,
                                           do_harvest: bool = True):
    yield RSFarmingMethod(name="{0} ({1}, {2}harvest)".format(data.name,
                                                              compost.name if compost is not None else "protect",
                                                              "" if do_harvest else "no "),
                          input_seq=chain(data.input_data,
                                          [(compost, 0.5 if bottomless_bucket else 1.0)]
                                          if compost is not None else data.payment_data),
                          output_seq=data.output_data if do_harvest else [],
                          num_per_hour=3600 / (data.time_walk_farm +
                                               (data.time_harvest if do_harvest else 0)),
                          plant_experience=data.plant_xp,
                          check_experience=data.check_xp,
                          harvest_experience=data.harvest_xp,
                          harvest_per_tree=data.harvest_amount,
                          cut_payment=cut_payment,
                          success_rate=calculate_success_rate(data.base_disease, data.steps, compost_rate))


def build_farm_methods(compostlist: Seq[Tuple[RSItem, float]], farmdata: Seq[FarmData],
                       bottomless_bucket: bool = False, cut_payment: int = 200):
    for staticdata in farmdata:
        for compost, compost_rate in chain(compostlist, [(None, 1)]):
            yield from _build_single_output_type_farm_methods(staticdata.clone(), compost, compost_rate,
                                                              bottomless_bucket, cut_payment, False)
            if staticdata.time_harvest > 0:
                yield from _build_single_output_type_farm_methods(staticdata.clone(), compost, compost_rate,
                                                                  bottomless_bucket, cut_payment, True)


def build_fruit_tree_list(db):
    stages = 6
    base_disease = 0.133
    fruit_trees = [
        FarmData(db, name="Apple trees",
                 plant_xp=22,
                 check_xp=1199.5,
                 harvest_xp=8.5,
                 inputs=[("apple sapling", 1)],
                 payments=[("sweetcorn", 9)],
                 outputs=[("cooking apple", 6)],
                 steps=stages,
                 base_disease=base_disease),
        FarmData(db, name="Banana trees",
                 inputs=[("banana sapling", 1)],
                 payments=[("apples", 4)],
                 outputs=[("banana", 6)],
                 plant_xp=28,
                 check_xp=1750.5,
                 harvest_xp=10.5,
                 steps=stages,
                 base_disease=base_disease),
        FarmData(db, name="orange trees",
                 inputs=[("orange sapling", 1)],
                 payments=[("strawberries", 3)],
                 outputs=[("orange", 6)],
                 plant_xp=35.5,
                 check_xp=2470.5,
                 harvest_xp=13.5,
                 steps=stages,
                 base_disease=base_disease),
        FarmData(db, name="Curry trees",
                 inputs=[("curry sapling", 1)],
                 payments=[("bananas", 5)],
                 outputs=[("curry leaf", 6)],
                 plant_xp=40,
                 check_xp=2906.9,
                 harvest_xp=15,
                 steps=stages,
                 base_disease=base_disease),
        FarmData(db, name="Pineapple trees",
                 inputs=[("pineapple sapling", 1)],
                 payments=[("watermelon", 10)],
                 outputs=[("pineapple", 6)],
                 plant_xp=57,
                 check_xp=4605.7,
                 harvest_xp=21.5,
                 steps=stages,
                 base_disease=base_disease),
        FarmData(db, name="Papaya trees",
                 inputs=[("papaya sapling", 1)],
                 payments=[("pineapple", 10)],
                 outputs=[("papaya fruit", 6)],
                 plant_xp=72,
                 check_xp=6146.4,
                 harvest_xp=27,
                 steps=stages,
                 base_disease=base_disease),
        FarmData(db, name="Palm trees",
                 inputs=[("palm sapling", 1)],
                 payments=[("papaya fruit", 15)],
                 outputs=[("coconut", 6)],
                 plant_xp=110.5,
                 check_xp=10150.1,
                 harvest_xp=41.50,
                 steps=stages,
                 base_disease=base_disease),
        FarmData(db, name="dragonfruit tree",
                 inputs=[("dragonfruit sapling", 1)],
                 payments=[("coconut", 15)],
                 outputs=[("dragonfruit", 6)],
                 plant_xp=140,
                 check_xp=17335,
                 harvest_xp=70,
                 steps=stages,
                 base_disease=base_disease)
    ]
    return fruit_trees,


def build_hardwood_list(db):
    hardwood_trees = [
        FarmData(db, name="Teak trees",
                 inputs=[("teak sapling", 1)],
                 payments=[("limpwurt root", 15)],
                 outputs=[],
                 plant_xp=35,
                 check_xp=7290,
                 harvest_xp=85,
                 time_harvest=25,
                 steps=7),
        FarmData(db, name="Mahogany trees",
                 inputs=[("mahogany sapling", 1)],
                 payments=[("yanillian hops", 25)],
                 outputs=[],
                 plant_xp=14,
                 check_xp=15720,
                 harvest_xp=125,
                 time_harvest=60,
                 steps=8)
    ]
    return hardwood_trees,


def build_other_farm_list(db):
    calquat_sappling = "calquat sapling"
    poison_ivy_berries = "poison ivy berries"
    calquat_fruit = "Calquat fruit"
    cactus_seed = "cactus seed"
    cadava_berries = "cadava berries"
    cactus_spine = "cactus spine"
    whiteberry_seed = "whiteberry seed"
    bittercap_mushrooms = "mushroom"
    white_berries = "white berries"
    poison_ivy_seed = "poison ivy seed"
    redwood_sapling = "redwood sapling"
    dragonfruits = "dragonfruit"

    calquat = [
        FarmData(db, name="calquat",
                 inputs=[(calquat_sappling, 1)],
                 payments=[(poison_ivy_berries, 8)],
                 outputs=[(calquat_fruit, 6)],
                 plant_xp=129.5,
                 check_xp=12096,
                 harvest_xp=48.5,
                 time_walk_farm=240,
                 steps=8)
    ]
    cactus = [
        FarmData(db, name="cactus",
                 inputs=[(cactus_seed, 1)],
                 payments=[(cadava_berries, 6)],
                 outputs=[(cactus_spine, 3)],
                 plant_xp=66.5,
                 check_xp=374,
                 harvest_xp=25,
                 steps=7)
    ]
    berries = [
        FarmData(db, name="whiteberry",
                 inputs=[(whiteberry_seed, 1)],
                 payments=[(bittercap_mushrooms, 8)],
                 outputs=[(white_berries, 4)],
                 plant_xp=66.5,
                 check_xp=374,
                 harvest_xp=25,
                 steps=8),
        FarmData(db, name="poison ivy",
                 inputs=[(poison_ivy_seed, 1)],
                 payments=[],
                 outputs=[(poison_ivy_berries, 4)],
                 plant_xp=120,
                 check_xp=675,
                 harvest_xp=45,
                 steps=8,
                 base_disease=0)
    ]
    redwood = [
        FarmData(db, name="redwood",
                 inputs=[(redwood_sapling, 1)],
                 payments=[(dragonfruits, 6)],
                 outputs=[],
                 plant_xp=230,
                 check_xp=22450,
                 harvest_xp=0,
                 steps=10)
    ]
    all_extra = (calquat, cactus, berries, redwood)
    return all_extra


def build_tree_list(db):
    oak_sapling = "oak sapling"
    tomato_basket = "tomatoes"
    willow_sapling = "willow sapling"
    basket_apples = "apples"
    maple_sapling = "maple sapling"
    basket_oranges = "oranges"
    yew_sapling = "yew sapling"
    cactus_spine = "cactus spine"
    magic_sappling = "magic sapling"
    coconut = "coconut"
    trees = [
        FarmData(db, name="Oak tree",
                 inputs=[(oak_sapling, 1)],
                 payments=[(tomato_basket, 1)],
                 outputs=[],
                 plant_xp=14,
                 check_xp=467.3,
                 harvest_xp=0,
                 time_harvest=20,
                 steps=5),
        FarmData(db, name="Willow trees",
                 inputs=[(willow_sapling, 1)],
                 payments=[(basket_apples, 1)],
                 outputs=[],
                 plant_xp=25,
                 check_xp=1456.5,
                 harvest_xp=0,
                 time_harvest=25,
                 steps=7),
        FarmData(db, name="Maple trees",
                 inputs=[(maple_sapling, 1)],
                 payments=[(basket_oranges, 2)],
                 outputs=[],
                 plant_xp=45,
                 check_xp=3403.4,
                 harvest_xp=0,
                 time_harvest=35,
                 steps=8,
                 base_disease=0.094),
        FarmData(db, name="Yew trees",
                 inputs=[(yew_sapling, 1)],
                 payments=[(cactus_spine, 10)],
                 outputs=[],
                 plant_xp=81,
                 check_xp=7069.9,
                 harvest_xp=0,
                 time_harvest=60,
                 steps=10),
        FarmData(db, name="Magic trees",
                 inputs=[(magic_sappling, 1)],
                 payments=[(coconut, 25)],
                 outputs=[],
                 plant_xp=145.5,
                 check_xp=13768.3,
                 harvest_xp=0,
                 time_harvest=120,
                 steps=12,
                 base_disease=0.063)
    ]
    return trees,


if __name__ == '__main__':
    compare_all_tree_farming("(?i)^(yew)", True)

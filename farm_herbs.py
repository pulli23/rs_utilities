from itertools import chain
from typing import Sequence as Seq
from typing import TypeVar, Tuple, List, Any
import math

from rs_money_methods import RSMoneyMethod, RSMethod
from rs_skill_method import RSFarmingMethod, RSSkillMethod, RSFarmingLazyMethod
from rs_item import RSItem, GPItem
import loader
from farm_main import FarmData, find_methods_by_name, calculate_success_rate


def build_herb_list(db, anima_seed: str = None, disease_free: bool = False) \
        -> Tuple[List[FarmData]]:
    disease = 1
    harvest_time = 10
    steps = 4
    base_harvest = 8
    output_mul = 1.1 if anima_seed == 'attas' else 1
    steps_mul = 0.9 if anima_seed == 'kronos' else 1
    disease_mul = 0 if disease_free else \
        (0.9 if anima_seed == 'iasor' else 1)

    herb = [
        FarmData(db, name='Guam ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('guam seed', 1)],
                 outputs=[('guam leaf', base_harvest * output_mul)],
                 plant_xp=11,
                 check_xp=0,
                 harvest_xp=12.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Marrentill ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Marrentill seed', 1)],
                 outputs=[('Marrentill', base_harvest * output_mul)],
                 plant_xp=13.5,
                 check_xp=0,
                 harvest_xp=15,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Tarromin ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Tarromin seed', 1)],
                 outputs=[('Tarromin', base_harvest * output_mul)],
                 plant_xp=16,
                 check_xp=0,
                 harvest_xp=18,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Harralander ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Harralander seed', 1)],
                 outputs=[('Harralander', base_harvest * output_mul)],
                 plant_xp=21.5,
                 check_xp=0,
                 harvest_xp=24,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Ranarr ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Ranarr seed', 1)],
                 outputs=[('Ranarr weed', base_harvest * output_mul)],
                 plant_xp=27,
                 check_xp=0,
                 harvest_xp=30.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Toadflax ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Toadflax seed', 1)],
                 outputs=[('Toadflax', base_harvest * output_mul)],
                 plant_xp=34,
                 check_xp=0,
                 harvest_xp=38.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Irit ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Irit seed', 1)],
                 outputs=[('Irit leaf', base_harvest * output_mul)],
                 plant_xp=43,
                 check_xp=0,
                 harvest_xp=48.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Avantoe ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Avantoe seed', 1)],
                 outputs=[('Avantoe', base_harvest * output_mul)],
                 plant_xp=54.5,
                 check_xp=0,
                 harvest_xp=61.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Kwuarm ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Kwuarm seed', 1)],
                 outputs=[('Kwuarm', base_harvest * output_mul)],
                 plant_xp=69,
                 check_xp=0,
                 harvest_xp=78,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Snapdragon ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Snapdragon seed', 1)],
                 outputs=[('Snapdragon', base_harvest * output_mul)],
                 plant_xp=87.5,
                 check_xp=0,
                 harvest_xp=98.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Cadantine ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Cadantine seed', 1)],
                 outputs=[('Cadantine', base_harvest * output_mul)],
                 plant_xp=106.5,
                 check_xp=0,
                 harvest_xp=120,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Lantadyme ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Lantadyme seed', 1)],
                 outputs=[('Lantadyme', base_harvest * output_mul)],
                 plant_xp=134.5,
                 check_xp=0,
                 harvest_xp=151.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Dwarf weed ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Dwarf weed seed', 1)],
                 outputs=[('Dwarf weed', base_harvest * output_mul)],
                 plant_xp=170.5,
                 check_xp=0,
                 harvest_xp=192,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
        FarmData(db, name='Torstol ({0}{1})'.format(anima_seed, ' disease free' if disease_free else ''),
                 inputs=[('Torstol seed', 1)],
                 outputs=[('Torstol', base_harvest * output_mul)],
                 plant_xp=199.5,
                 check_xp=0,
                 harvest_xp=224.5,
                 time_harvest=harvest_time,
                 base_disease=disease * disease_mul,
                 steps=steps * steps_mul,
                 ),
    ]
    return herb,


def _build_herb_type_farm_methods(data: FarmData, compost: RSItem, compost_rate: float,
                                  compost_modified: float, bottomless_bucket: bool = False,
                                  resurrect_items: Seq[Tuple[RSItem, float]] = None):
    will_resurrect = False
    input_seq = list(chain(data.input_data,
                           [(compost, 0.5 if bottomless_bucket else 1.0)]))  # type: List[Tuple[RSItem, float]]

    if resurrect_items is not None:
        resurrect_price = sum(item.current_price * num for item, num in resurrect_items)
        input_price = sum(item.current_price * num for item, num in input_seq)
        will_resurrect = resurrect_price < 0.75 * input_price

    chance_to_resurrect = \
        1 - calculate_success_rate(data.base_disease, data.steps, compost_rate, False) \
        if will_resurrect else 0

    success_chance = calculate_success_rate(data.base_disease, data.steps, compost_rate, will_resurrect)
    if will_resurrect:
        for item, num in resurrect_items:
            input_seq.append((item, num * chance_to_resurrect))

    output = []
    for (item, num) in data.output_data:
        modified_num = compost_modified * num
        output.append((item, modified_num))

    yield RSFarmingMethod(name="{0} ({1} resurrect: {2})".format(data.name, compost.name, will_resurrect),
                          input_seq=input_seq,
                          output_seq=output,
                          num_per_hour=3600 / (data.time_walk_farm +
                                               (data.time_harvest)),
                          plant_experience=data.plant_xp,
                          check_experience=data.check_xp,
                          harvest_experience=data.harvest_xp,
                          harvest_per_tree=data.harvest_amount * compost_modified,
                          cut_payment=0,
                          success_rate=success_chance)


def build_farm_methods(compostlist: Seq[Tuple[RSItem, float, float]], farmdata: Seq[FarmData],
                       bottomless_bucket: bool = False,
                       resurrect_items: Seq[Tuple[RSItem, float]] = None):
    for staticdata in farmdata:
        for compost, compost_rate, compost_modifier in compostlist:
            d = staticdata.clone()
            # modify d's output
            yield from _build_herb_type_farm_methods(d,
                                                     compost,
                                                     compost_rate,
                                                     compost_modifier,
                                                     bottomless_bucket,
                                                     resurrect_items)


def compare_methods(methods: List[RSSkillMethod]):
    methods.sort(key=lambda x: x.profit_per_hour, reverse=True)
    strlen = max(len(x.name) for x in methods)
    max_experience_per_hour = 0
    for method in methods:
        if method.experience_per_hour > max_experience_per_hour:
            max_experience_per_hour = method.experience_per_hour
            print('{:<{length}} | {profit:.6} | {xp:.5}'.format(method.name,
                                                                length=strlen,
                                                                profit=method.profit_per_item,
                                                                xp=method.experience_per_item))


def compare_all_herb_farming(name_pattern: str = None, bottomless_bucket: bool = False, allow_resurrect: bool = True):
    db = loader.DataOSRSGE()
    composts = ((RSItem(db.find_best_item("supercompost")), 1 / 8, 5 / 6),
                (RSItem(db.find_best_item("ultracompost")), 1 / 10, 1))
    resurrect_crops_items = None
    if allow_resurrect:
        resurrect_crops_items = [(RSItem(db.find_best_item("soul rune")), 8),
                                 (RSItem(db.find_best_item("nature rune")), 12),
                                 (RSItem(db.find_best_item("blood rune")), 8)]

    for c in composts:
        print(c[0], c[0].current_price)

    allfarmmethods = []
    allfarmmethods.extend(build_herb_list(db))
    allfarmmethods.extend(build_herb_list(db, 'attas'))
    allfarmmethods.extend(build_herb_list(db, 'iasor'))
    allfarmmethods.extend(build_herb_list(db, 'kronos'))
    allfarmmethods.extend(build_herb_list(db, None, True))
    allfarmmethods.extend(build_herb_list(db, 'attas', True))
    build_methods = []
    for method in allfarmmethods:
        l = list(build_farm_methods(composts, method, bottomless_bucket, resurrect_crops_items))
        build_methods.extend(l)
        compare_methods(l)
        print("--------------")

    print("--------------")
    if name_pattern:
        methods = find_methods_by_name(build_methods, name_pattern)
        for m in methods:
            print(m)

    return allfarmmethods


if __name__ == '__main__':
    compare_all_herb_farming("(?i)^(ranarr)", False, True)

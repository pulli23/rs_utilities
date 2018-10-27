from itertools import chain

from rs_money_methods import RSMoneyMethod, RSMethod
from rs_skill_method import RSSkillMethod, RSLazySkillMethod
from rs_item import RSItem, GPItem
import loader


def compare_all_smelting():
    db = loader.DataOSRSGE()

    stamina_pot = RSItem(db.find_best_item("stamina potion"))
    gp = GPItem()
    coal = RSItem(db.find_best_item("coal"))
    methods = []
    methods.append(create_smelting_method(db,
                                          name="gold bar",
                                          in_names=[("gold ore", 1)],
                                          out_names=[("gold bar", 1)],
                                          coal_amount=0,
                                          num_per_hour=6000,
                                          hourly_input=[("stamina potion", 6)],
                                          exp_per_item=56.2))

    methods.append(create_smelting_method(db,
                                          name="steel bar",
                                          in_names=[("iron ore", 1)],
                                          out_names=[("steel bar", 1)],
                                          coal_amount=1,
                                          num_per_hour=4200,
                                          hourly_input=[("stamina potion", 6)],
                                          exp_per_item=17.5))

    methods.append(create_smelting_method(db,
                                          name="mithril bar",
                                          in_names=[("mithril ore", 1)],
                                          out_names=[("mithril bar", 1)],
                                          coal_amount=2,
                                          num_per_hour=3000,
                                          hourly_input=[("stamina potion", 6.5)],
                                          exp_per_item=30))

    methods.append(create_smelting_method(db,
                                          name="adamantite bar",
                                          in_names=[("adamantite ore", 1)],
                                          out_names=[("adamantite bar", 1)],
                                          coal_amount=3,
                                          num_per_hour=2335,
                                          hourly_input=[("stamina potion", 6.75)],
                                          exp_per_item=37.5))

    methods.append(create_smelting_method(db,
                                          name="runite bar",
                                          in_names=[("runite ore", 1)],
                                          out_names=[("runite bar", 1)],
                                          coal_amount=4,
                                          num_per_hour=2400 * (2/5) / (1/2),
                                          hourly_input=[("stamina potion", 7)],
                                          exp_per_item=50))
    methods.sort(key=lambda x: x.profit_per_hour)
    for method in methods:
        print(method.input_price)
        print("{name} | {profit} | {xp} | {gpitem}".format(name=method.name,
                                                           profit=method.profit_per_hour,
                                                           xp=method.experience_per_hour,
                                                           gpitem=method.profit_per_item))

    print(methods[-1])
    print(methods[-1].rate)



def create_smelting_method(db, name: str, in_names, out_names, coal_amount, num_per_hour, hourly_input, exp_per_item):
    coal = RSItem(db.find_best_item("coal"))
    method = RSSkillMethod(name=name,
                           input_seq=chain(((RSItem(db.find_best_item(name)), num) for name, num in in_names),
                                           [(coal, coal_amount)]),
                           output_seq=((RSItem(db.find_best_item(name)), num) for name, num in out_names),
                           num_per_hour=num_per_hour,
                           hourly_input_seq=chain(((RSItem(db.find_best_item(name)), num)
                                                   for name, num in hourly_input),
                                                  [(GPItem(), 72000)]),
                           exp_per_item=exp_per_item)
    return method

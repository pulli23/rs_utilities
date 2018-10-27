from typing import Iterable, Tuple, List, MutableSequence
import itertools

import rs_item
from rs_money_methods import RSMethod, RSLazyMethod


class RSSkillMethod(RSMethod):
    def __init__(self,
                 name: str=None,
                 input_seq: Iterable[Tuple[rs_item.RSItem, float]]=None,
                 output_seq: Iterable[Tuple[rs_item.RSItem, float]]=None,
                 num_per_hour: float=None,
                 exp_per_item: float=0,
                 *args, **kwargs):
        super().__init__(name=name, input_seq=input_seq, output_seq=output_seq,
                         num_per_hour=num_per_hour, *args, **kwargs)
        self._exp_per_item = exp_per_item

    @property
    def experience_per_item(self) -> float:
        return self._exp_per_item

    @property
    def experience_per_hour(self) -> float:
        return self._exp_per_item * self.rate

    @property
    def gp_per_xp(self) -> float:
        return self.profit_per_item/self.experience_per_item


class RSLazySkillMethod(RSSkillMethod, RSLazyMethod):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RSFarmingMethod(RSSkillMethod):
    def __init__(self, name=None, input_seq: MutableSequence[Tuple[rs_item.RSItem, float]]=None,
                 output_seq: Iterable[Tuple[rs_item.RSItem, float]]=None, num_per_hour: float=None,
                 plant_experience: float=0, check_experience: float=0, harvest_experience: float=0,
                 harvest_per_tree: float=6, success_rate: float=7./8., cut_payment: float=200., *args, **kwargs):
        if input_seq is None:
            input_seq = []
        itertools.chain(input_seq, (rs_item.GPItem(), success_rate * cut_payment))
        if output_seq is not None:
            output_seq = ((item, num * success_rate) for item, num in output_seq)
        exp_per_item = plant_experience + (check_experience + harvest_experience * harvest_per_tree) * success_rate
        super().__init__(name, input_seq, output_seq, num_per_hour, exp_per_item, *args, **kwargs)


class RSFarmingLazyMethod(RSFarmingMethod, RSLazyMethod):
    pass

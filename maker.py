from enum import Enum
from math import floor, ceil
from random import random
from functools import wraps

from objects import Player, Recipe, Buffs
from tables import Tables, ConditionModifier

T = Tables()


def action(cost: int = 0, durability_loss: int = 0):
    """decorator for actions. Remove CP and durability"""
    def callable(func):
        @wraps(func)
        def wrapper(self):
            func(self)
            self.player.cp -= cost
            self.update_durability(durability_loss)
            self.buffs.update()
            print(self.durability, self.progress, self.quality, self.player.cp)
            return self
        return wrapper

    return callable


class Maker:

    def __init__(self, player: Player, recipe: Recipe):
        self.player = player
        self.recipe = recipe
        self.diff = T.get_crafter_level(player.level) - recipe.rlevel

        self.progress = 0
        self.quality = 0
        self.durability = recipe.durability

        self.buffs = Buffs()
        self.condition = ConditionModifier.Normal

    def increase_progress(self, efficiency, brand=False):
        p1 = self.player.craftsmanship * 21 / 100 + 2
        p2 = p1 * (self.player.craftsmanship + 10000) / (self.recipe.craftsmanship + 10000)
        p3 = p2 * T.get_level_mod(self.diff, progress=True) / 100
        progress = floor(floor(p3) * self.calc_progress_efficiency(efficiency, brand=brand))

        self.progress += floor(progress / 100)

        if self.buffs.final_appraisal and self.progress > self.recipe.progress:
            self.buffs.final_appraisal = 0
            self.progress = self.recipe.progress - 1

        return self

    def increase_quality(self, efficiency):
        q1 = self.inner_quiet_bonus * 35 / 100 + 35

        q2 = q1 * (self.inner_quiet_bonus + 10000) / (self.recipe.control + 10000)

        q3 = q2 * T.get_level_mod(self.diff, progress=False) / 100

        quality = floor(floor(q3 * self.condition_bonus) * self.calc_quality_efficiency(efficiency))

        self.quality += floor(quality / 100)

        if self.buffs.inner_quiet_active:
            self.buffs.inner_quiet += 1

        return self

    def calc_progress_efficiency(self, efficiency, brand=False):
        eff = efficiency * (100 + sum(self.buffs.progress_buff_list)) / 100
        if brand and self.buffs.name_of_the_elements:
            eff += self.name_of_the_elements_bonus
        return eff

    def calc_quality_efficiency(self, efficiency):
        return efficiency * (100 + sum(self.buffs.quality_buff_list)) / 100

    @property
    def inner_quiet_bonus(self):
        bonus = self.player.control + self.player.control * ((self.buffs.inner_quiet - 1) * 20 / 100)
        return bonus

    @property
    def condition_bonus(self) -> float:
        return self.condition.value/100

    @property
    def byregot_blessing_bonus(self) -> int:
        return 100 + (self.buffs.inner_quiet - 1) * 20

    @property
    def name_of_the_elements_bonus(self) -> int:
        return 2 * ceil((1 - self.progress / self.recipe.progress) * 100)

    def durability_loss(self, durability_cost):
        if self.buffs.waste_not == 0:
            return durability_cost
        else:
            return durability_cost / 2

    def update_durability(self, durability_cost):
        if durability_cost:
            self.durability -= self.durability_loss(durability_cost)
        if self.buffs.manipulation:
            self.durability += 5

    # list of abilities - Progression

    @action(durability_loss=10)
    def basic_synthesis(self):
        self.increase_progress(120)

    @action(cost=7, durability_loss=10)
    def careful_synthesis(self):
        self.increase_progress(150)

    @action(durability_loss=10)
    def rapid_synthesis(self):

        if random() < 0.5:
            self.increase_progress(500)

    @action(cost=18, durability_loss=20)
    def groundwork(self):
        if self.durability < self.durability_loss(20):
            self.increase_progress(150)
        else:
            self.increase_progress(300)

    @action(cost=5, durability_loss=10)
    def focused_synthesis(self):
        raise NotImplemented

    @action(cost=6, durability_loss=10)
    def muscle_memory(self):
        raise NotImplemented

    @action(cost=6, durability_loss=10)
    def brand_of_the_elements(self):
        self.increase_progress(100, brand=True)

    @action(cost=6, durability_loss=10)
    def intensive_synthesis(self):
        if self.condition != ConditionModifier.Good and self.condition != ConditionModifier.Excellent:
            raise Exception('Cannot use when not Good or Excellent')
        else:
            raise NotImplemented

    # list of abilities - Quality

    @action(cost=18, durability_loss=10)
    def basic_touch(self):
        self.increase_quality(100)

    @action(cost=32, durability_loss=10)
    def standard_touch(self):
        self.increase_quality(125)

    @action(durability_loss=10)
    def hasty_touch(self):
        if random() < 0.6:
            self.increase_quality(125)

    @action(cost=24, durability_loss=10)
    def byregots_blessing(self):
        raise NotImplemented

    @action(cost=18, durability_loss=10)
    def precise_touch(self):
        raise NotImplemented

    @action(cost=18, durability_loss=10)
    def focused_touch(self):
        raise NotImplemented

    @action(cost=6, durability_loss=10)
    def patient_touch(self):
        raise NotImplemented

    @action(cost=25, durability_loss=5)
    def prudent_touch(self):
        if self.buffs.waste_not != 0:
            raise Exception('cant use skill with waste not active')
        else:
            self.increase_quality(100)

    @action(cost=150, durability_loss=10)
    def trained_eye(self):
        raise NotImplemented

    @action(cost=40, durability_loss=10)
    def preparatory_touch(self):
        raise NotImplemented

    @action(cost=24, durability_loss=10)
    def reflect(self):
        raise NotImplemented

    # list of abilities - Buffs

    @action(cost=18)
    def inner_quiet(self):
        self.buffs.inner_quiet_active = True

    @action(cost=56)
    def waste_not(self):
        self.buffs.waste_not = 4 + 1

    @action(cost=98)
    def waste_not_ii(self):
        self.buffs.waste_not = 8 + 1

    @action(cost=32)
    def great_strides(self):
        raise NotImplemented

    @action(cost=18)
    def innovation(self):
        raise NotImplemented

    @action(cost=18)
    def veneration(self):
        raise NotImplemented

    @action(cost=30)
    def name_of_the_elements(self):
        if self.buffs.name_of_the_elements_available:
            self.buffs.name_of_the_elements_available = False
            self.buffs.name_of_the_elements = 3 + 1
        else:
            raise Exception('Already used this action in synthesis')

    @action(cost=1)
    def final_appraisal(self):
        self.buffs.final_appraisal = 5 + 1

    # list of abilities - Repair

    @action(cost=88)
    def masters_mend(self):
        self.durability += 30

    @action(cost=96)
    def manipulation(self):
        self.buffs.manipulation = 8 + 1

    # list of abilities - Other

    @action(cost=7)
    def observe(self):
        pass

    @action()
    def careful_observation(self):
        raise NotImplemented

    @action(cost=32)
    def delicate_synthesis(self):
        self.increase_progress(100)
        self.increase_quality(100)

    @action()
    def tricks_of_the_trade(self):
        if self.condition == ConditionModifier.Good or self.condition == ConditionModifier.Excellent:
            self.player.cp += 20
        else:
            raise Exception('Can only use when Good condition.')


class Actions(Enum):
    # progression
    BASIC_SYNTHESIS = Maker.basic_synthesis.__name__
    CAREFUL_SYNTHESIS = Maker.careful_synthesis.__name__
    RAPID_SYNTHESIS = Maker.rapid_synthesis.__name__
    GROUNDWORK = Maker.groundwork.__name__
    FOCUSED_SYNTHESIS = Maker.focused_synthesis.__name__
    MUSCLE_MEMORY = Maker.muscle_memory.__name__
    BRAND_OF_THE_ELEMENTS = Maker.brand_of_the_elements.__name__
    INTENSIVE_SYNTHESIS = Maker.intensive_synthesis.__name__

    # quality
    BASIC_TOUCH = Maker.basic_touch.__name__
    STANDARD_TOUCH = Maker.standard_touch.__name__
    HASTY_TOUCH = Maker.hasty_touch.__name__
    BYREGOTS_BLESSING = Maker.byregots_blessing.__name__
    PRECISE_TOUCH = Maker.prudent_touch.__name__
    FOCUSED_TOUCH = Maker.focused_touch.__name__
    PATIENT_TOUCH = Maker.patient_touch.__name__
    PRUDENT_TOUCH = Maker.prudent_touch.__name__
    TRAINED_EYE = Maker.trained_eye.__name__
    PREPARATORY_TOUCH = Maker.preparatory_touch.__name__
    REFLECT = Maker.reflect.__name__

    # buff
    INNER_QUIET = Maker.inner_quiet.__name__
    WASTE_NOT = Maker.waste_not.__name__
    WASTE_NOT_II = Maker.waste_not_ii.__name__
    GREAT_STRIDES = Maker.great_strides.__name__
    INNOVATION = Maker.innovation.__name__
    VENERATION = Maker.veneration.__name__
    NAME_OF_THE_ELEMENTS = Maker.name_of_the_elements.__name__
    FINAL_APPRAISAL = Maker.final_appraisal.__name__

    # repair
    MASTERS_MEND = Maker.masters_mend.__name__
    MANIPULATION = Maker.manipulation.__name__

    # other
    OBSERVE = Maker.observe.__name__
    CAREFUL_OBSERVATION = Maker.careful_synthesis.__name__
    DELICATE_SYNTHESIS = Maker.delicate_synthesis.__name__
    TRICKS_OF_THE_TRADE = Maker.tricks_of_the_trade.__name__

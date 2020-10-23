
class Buffs:
    MUSCLE_MEMORY = "Muscle memory"
    INNER_QUIET = "Inner Quiet"
    WASTE_NOT = "Waste_not"
    GREAT_STRIDES = "Great_Stride"
    INNOVATION = "Innovation"
    VENERATION = "Veneration"
    NAME_OF_THE_ELEMENTS = "Name of the elements"
    FINAL_APPRAISAL = "Final Appraisal"
    MANIPULATION = "Manipulation"
    OBSERVE = "Observe"


class Buff:

    def __init__(self, initial_value):
        self.initial_value = initial_value
        self.value = 0
        self.active = False
        self.activated = False

    def update(self):
        if self.activated:
            self.active = True
            self.activated = False
            self.value = self.initial_value

        elif self.value > 0:
            self.value -= 1

        if self.value == 0 and self.active:
            self.active = False

    def activate(self):
        self.activated = True

    def lose(self):
        self.active = False
        self.value = 0


class InnerQuiet(Buff):

    def __init__(self, initial_value):
        super().__init__(initial_value)
        self.value = 1

    def update(self):
        if self.activated:
            self.active = True
            self.activated = False

    def increase(self):
        if self.active and self.value < 11:
            self.value += 1

    def double(self):
        if self.active:
            self.value *= 2
            if self.value > 11:
                self.value = 11

    def half(self):
        if self.active:
            self.value //= 2

    def lose(self):
        self.active = False
        self.value = 1


class NameOfTheElements(Buff):

    def __init__(self, initial_value):
        super().__init__(initial_value)
        self.available = True

    def activate(self):
        if self.available:
            self.activated = True
            self.available = False
        else:
            raise Exception('Already used this action in synthesis')


class MakerBuffs:

    def __init__(self):
        self.muscle_memory = Buff(5)
        self.inner_quiet = InnerQuiet(0)
        self.waste_not = Buff(4)
        self.waste_not_ii = Buff(8)
        self.great_strides = Buff(3)
        self.innovation = Buff(4)
        self.veneration = Buff(4)
        self.name_of_the_elements = NameOfTheElements(3)
        self.final_appraisal = Buff(5)
        self.manipulation = Buff(8)
        self.observe = Buff(1)

    @property
    def progress_buff_list(self):
        return [
            50 if self.veneration.active else 0,
            100 if self.muscle_memory.active else 0
        ]

    @property
    def quality_buff_list(self):
        return [
            100 if self.great_strides.active else 0,
            50 if self.innovation.active else 0
        ]

    def update(self):
        self.muscle_memory.update()
        self.inner_quiet.update()
        self.waste_not.update()
        self.waste_not_ii.update()
        self.great_strides.update()
        self.innovation.update()
        self.veneration.update()
        self.name_of_the_elements.update()
        self.final_appraisal.update()
        self.manipulation.update()
        self.observe.update()

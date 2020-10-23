from math import floor

from database import FFXIVDB


class Stats:

    def __init__(self, craftsmanship, control, cp):
        self.craftsmanship = craftsmanship
        self.control = control
        self.cp = cp

    def __add__(self, other):
        self.craftsmanship += other.craftsmanship
        self.control += other.control
        self.cp += other.cp
        return self


class Player(Stats):

    def __init__(self, level, craftsmanship, control, cp):
        super().__init__(craftsmanship, control, cp)
        self.level = level


class Recipe:

    def __init__(self, name):
        self.name = name

        self.rlevel = None

        self.progress = None
        self.quality = None
        self.durability = None

        self.control = None
        self.craftsmanship = None

        self.star = None
        self.expert = False

    def update_fromdb(self):
        client = FFXIVDB()
        recipe_data = client.get_recipe_by_name(self.name)

        self.rlevel = recipe_data['RecipeLevelTableTargetID']

        durability_base = recipe_data['RecipeLevelTable']['Durability']
        durability_factor = recipe_data['DurabilityFactor']
        self.durability = floor(durability_base * durability_factor / 100)

        progress_base = recipe_data['RecipeLevelTable']['Difficulty']
        progress_factor = recipe_data['DifficultyFactor']
        self.progress = floor(progress_base * progress_factor / 100)

        quality_base = recipe_data['RecipeLevelTable']['Quality']
        quality_factor = recipe_data['QualityFactor']
        self.quality = floor(quality_base * quality_factor / 100)

        self.control = recipe_data['RecipeLevelTable']['SuggestedControl']
        self.craftsmanship = recipe_data['RecipeLevelTable']['SuggestedCraftsmanship']

        self.star = recipe_data['RecipeLevelTable']['Stars']
        self.expert = recipe_data['IsExpert']


class Buffs:

    def __init__(self):
        self.inner_quiet = 1
        self.inner_quiet_active = False
        self.waste_not = 0
        self.great_strides = 0
        self.innovation = 0
        self.veneration = 0
        self.name_of_the_elements = 0
        self.name_of_the_elements_available = True
        self.final_appraisal = 0
        self.manipulation = 0

    @property
    def progress_buff_list(self):
        return [50 if self.veneration != 0 else 0]

    @property
    def quality_buff_list(self):
        return [
            100 if self.great_strides != 0 else 0,
            50 if self.innovation != 0 else 0
        ]

    def update(self):

        if self.waste_not:
            self.waste_not -= 1

        if self.great_strides:
            self.great_strides -= 1

        if self.innovation:
            self.innovation -= 1

        if self.final_appraisal:
            self.final_appraisal -= 1

        if self.name_of_the_elements:
            self.name_of_the_elements -= 1

        if self.manipulation:
            self.manipulation -= 1

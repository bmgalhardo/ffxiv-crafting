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

    def available_actions(self):
        from maker import Actions

        action_available = []
        for action in Actions:
            if action.value.min_level < self.level:
                action_available.append(action.name)
        return action_available

    def check_rotation(self, rotation: list):
        for action in rotation:
            if action.value.min_level > self.level:
                raise Exception(f'{action.name} not available at lvl {self.level}')


class Recipe:

    def __init__(self, name):
        self.name = name

        self.level = None
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

        self.level = recipe_data['RecipeLevelTable']['ClassJobLevel']
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


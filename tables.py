from enum import Enum
import pandas as pd


class ConditionModifier(Enum):
    Poor = 50
    Normal = 100
    Good = 150
    Excellent = 400


class Tables:

    def __init__(self):
        self.level_mod = pd.read_csv("tables/LevelMod.csv")
        self.crafter_level_by_index = [i for i in range(1, 51)] + [
            120,
            125,
            130,
            133,
            136,
            139,
            142,
            145,
            148,
            150,
            260,
            265,
            270,
            273,
            276,
            279,
            282,
            285,
            288,
            290,
            390,
            395,
            400,
            403,
            406,
            409,
            412,
            415,
            418,
            420,
        ]

    def get_crafter_level(self, level):
        return self.crafter_level_by_index[level-1]

    def get_level_mod(self, diff, progress=True):
        if diff < -30:
            diff = -30
        elif diff > 20:
            diff = 20

        value = self.level_mod.loc[self.level_mod.DIFF == diff]['PROGRESS' if progress else 'QUALITY'].iloc[0]
        return value

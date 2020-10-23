import requests
from pprint import pprint


class FFXIVDB:

    def __init__(self):
        self.main_address = "https://xivapi.com"
        self.private_key = "d8044ca21dd848fd996badf8a98bc4d578cc77c365c5454d9f86b1b6eec6e6ff"
        self.string_algos = [
            "custom", "wildcard", "wildcard_plus", "fuzzy", "term", "prefix", "match", "match_phrase",
            "match_phrase_prefix", "multi_match", "query_string"
        ]

    def get_recipe_by_id(self, id, cols=None):
        endpoint = f"{self.main_address}/recipe/{id}?private_key={self.private_key}"
        if cols:
            endpoint += f"&columns={','.join(cols)}"
        response = requests.get(endpoint)
        pprint(response.json())

    def get_recipe_by_name(self, name, string_algo='match'):

        cols = [
            'QualityFactor',
            'DifficultyFactor',
            'DurabilityFactor',
            'IsExpert',
            'QualityFactor',
            'RecipeLevelTable',
            'RecipeLevelTableTarget',
            'RecipeLevelTableTargetID',
            # 'RequiredControl',
            # 'RequiredCraftsmanship',
        ]

        if string_algo not in self.string_algos:
            raise Exception(f'"{string_algo}" is not a supported string_algo for XIVAPI')

        endpoint = f"{self.main_address}/search?language=en&private_key={self.private_key}"

        body = {
            "indexes": 'Recipe',
            "columns": "ID" if cols is None else ','.join(cols),
            "body": {
                "query": {
                    "bool": {
                        "should": [{
                            string_algo: {
                                "NameCombined_en": {
                                    "query": name,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 1,
                                    "max_expansions": 50
                                }
                            }
                        }]
                    }
                }
            }
        }

        response = requests.post(endpoint, json=body)
        result = response.json()['Results']

        if len(result) > 1:
            raise Exception('More than 1 recipe!')
        elif len(result) == 0:
            raise Exception('No recipe found!')

        # print(result)
        return result[0]

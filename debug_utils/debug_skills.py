
import json
import time
import os
from monster_skill import MonsterSkill
from skill_type_maps import SKILL_TYPE


with open('skills.json', 'r+') as jsonPull:
    jsonData = json.load(jsonPull)

    print()
    print("Building skill list.")
    print()
    for i, ms in enumerate(jsonData['skill']):
        try:
            parsed_skill = MonsterSkill(i, ms)
        except:
            print('Error at', i)
            print('MS:', ms)

    print('Skill build complete')

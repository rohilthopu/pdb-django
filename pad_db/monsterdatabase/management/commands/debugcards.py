from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import Skill
import requests
import json
from .skill_parser import parse_skill_multiplier
from .skill_info import reformat_json
import math
import time

passed_tests = 0
failed_tests = 0

class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        def getMultipliers(skill) -> []:
            skill_list = []
            multipliers = [1, 1, 1, 0]
            shield_calc = 1
            shields = []
            if skill.c_skill_1 != -1:
                skill_list.append(Skill.objects.get(skillID=skill.c_skill_1))
                skill_list.append(Skill.objects.get(skillID=skill.c_skill_2))
                if skill.c_skill_3 != -1:
                    skill_list.append((Skill.objects.get(skillID=skill.c_skill_3)))

                for skill in skill_list:

                    multipliers[0] *= skill.hp_mult
                    multipliers[1] *= skill.atk_mult
                    multipliers[2] *= skill.rcv_mult
                    if skill.dmg_reduction != 0:
                        shields.append(skill.dmg_reduction)

                for shield in shields:
                    shield_calc *= (1 - shield)

                multipliers[0] = round(multipliers[0], 3)
                multipliers[1] = round(multipliers[1], 3)
                multipliers[2] = round(multipliers[2], 3)
                multipliers[3] = float( round((1 - shield_calc), 3))
            else:
                multipliers[0] = skill.hp_mult
                multipliers[1] = skill.atk_mult
                multipliers[2] = skill.rcv_mult
                multipliers[3] = float(skill.dmg_reduction)
            return multipliers

        def testSkill(info):
            args = info['args']
            if len(args) != 0:
                if 'parameter' in args:
                    mults = args['parameter']

                    right = 0
                    for i in range(0, len(multipliers)):
                        if multipliers[i] == mults[i]:
                            right += 1
                        else:
                            print()
                            print("Incorrect values at index", i, "with values", multipliers[i], mults[i])

                    if right != 4:
                        global failed_tests
                        failed_tests += 1
                        print("Failed test on skill", skill.name, skill.skillID)
                        print('\t\tSkill Description', skill.description)
                        print("\t\t\t\tMy calculated multipliers:", multipliers)
                        print("\t\t\t\t\t\tValidated results:", mults)
                        print()
                    else:
                        # print("Test for skill", skill.name, ", Skill ID", skill.skillID, "passed!")
                        global  passed_tests
                        passed_tests += 1

        link = "https://storage.googleapis.com/mirubot/paddata/raw/jp/download_skill_data.json"

        skills = Skill.objects.all()

        req = requests.get(link).text
        data = json.loads(req)
        parse = reformat_json(data)
        parsed = parse['leader_skills']
        a_skills = parse['active_skills']

        start = time.time()

        for skill in skills:
            s_id = skill.skillID
            multipliers = getMultipliers(skill)

            # if s_id in parsed:
            #     print(parsed[s_id])
            if s_id in parsed:
                info = parsed[s_id]
                testSkill(info)
            elif s_id in a_skills:
                info = a_skills[s_id]
                testSkill(info)

        end = time.time()
        print("Tests passed:", passed_tests)
        print("Tests failed:", failed_tests)
        print("Elapsed time:", end - start, "seconds.")

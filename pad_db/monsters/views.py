from django.shortcuts import render
from django.http import JsonResponse
from .models import Monster
from skills.models import Skill
from .maps import EXPLICIT_TYPE_MAP
import json
from dungeons.models import Dungeon, Floor


def monster_view(request, card_id):
    template = 'monster_na.html'
    monster = Monster.objects.get(card_id=card_id)
    evo_list = json.loads(monster.evolutions)
    monsters = Monster.objects.all()

    # The following set of checks is necessary as some cards do not have leader skills, active skills, or ancestors.
    ancestor = None
    if monster.ancestor_id != monster.card_id:
        if monster.ancestor_id != 0:
            ancestor = Monster.objects.get(card_id=monster.ancestor_id)

    active_skill = None
    leader_skill = None

    if Skill.objects.filter(skill_id=monster.active_skill_id).first() is not None:
        active_skill = Skill.objects.get(skill_id=monster.active_skill_id)
    if Skill.objects.filter(skill_id=monster.leader_skill_id).first() is not None:
        leader_skill = Skill.objects.get(skill_id=monster.leader_skill_id)

    multipliers = [1, 1, 1, 0, 0]
    a_multipliers = [1, 1, 1, 0]

    if leader_skill is not None:
        multipliers = get_multipliers(leader_skill)

    if active_skill is not None:
        a_multipliers = get_multipliers(active_skill)

    d_multipliers = [round((item ** 2), 2) for item in multipliers]
    d_multipliers[3] = round((1 - (1 - multipliers[4]) * (1 - multipliers[4])) * 100, 2)

    evos = None
    if len(evo_list) > 0:
        evos = get_evos(evo_list)

    evo_mats = get_evo_mats(monster, monsters)
    unevo_mats = get_unevo_mats(monster, monsters)

    awakenings = json.loads(monster.awakenings)
    super_awakenings = json.loads(monster.super_awakenings)

    types = get_types(monster)

    dungeons = get_dungeons(card_id)

    context = {'active_skill': active_skill, 'leader_skill': leader_skill,
               'monster': monster, 'ancestor': ancestor, "evolutions": evos, "evo_mats": evo_mats,
               "unevo_mats": unevo_mats, 'awakenings': awakenings, 'super_awakenings': super_awakenings, 'types': types,
               'lmultipliers': multipliers, 'dmultipliers': d_multipliers, 'amultipliers': a_multipliers,
               'dungeons': dungeons}

    return render(request, template, context)


def monster_list(request):
    rawCards = Monster.objects.order_by('cardID').all()
    cards = []
    cardID = []

    for card in rawCards:
        if "*" not in card.name:
            if "Alt." not in card.name:
                cards.append(card.name)
                cardID.append(card.cardID)

    cardList = zip(cards, cardID)
    context = {'cards': cardList}
    template = 'monster_list_na.html'
    return render(request, template, context)


def get_evo_mats(monster, monsters):
    evo_mats = []
    if monster.evo_mat_1 != 0:
        evo_mats.append(monsters.get(card_id=monster.evo_mat_1))
    if monster.evo_mat_2 != 0:
        evo_mats.append(monsters.get(card_id=monster.evo_mat_2))
    if monster.evo_mat_3 != 0:
        evo_mats.append(monsters.get(card_id=monster.evo_mat_3))
    if monster.evo_mat_4 != 0:
        evo_mats.append(monsters.get(card_id=monster.evo_mat_4))
    if monster.evo_mat_5 != 0:
        evo_mats.append(monsters.get(card_id=monster.evo_mat_5))
    return evo_mats


def get_unevo_mats(monster, monsters):
    unevo_mats = []
    if monster.unevo_mat_1 != 0:
        unevo_mats.append(monsters.get(cardID=monster.unevo_mat_1))
    if monster.unevo_mat_2 != 0:
        unevo_mats.append(monsters.get(cardID=monster.unevo_mat_2))
    if monster.unevo_mat_3 != 0:
        unevo_mats.append(monsters.get(cardID=monster.unevo_mat_3))
    if monster.unevo_mat_4 != 0:
        unevo_mats.append(monsters.get(cardID=monster.unevo_mat_4))
    if monster.unevo_mat_5 != 0:
        unevo_mats.append(monsters.get(cardID=monster.unevo_mat_5))
    return unevo_mats


def get_types(monster) -> []:
    types = [EXPLICIT_TYPE_MAP[monster.type_1], EXPLICIT_TYPE_MAP[monster.type_2],
             EXPLICIT_TYPE_MAP[monster.type_3]]
    return types


def get_multipliers(skill) -> []:
    skill_list = []
    multipliers = [1, 1, 1, 0, 0]
    shield_calc = 1
    shields = []
    if skill.skill_part_1_id != -1:
        skill_list.append(Skill.objects.get(skill_id=skill.skill_part_1_id))
        skill_list.append(Skill.objects.get(skill_id=skill.skill_part_2_id))
        if skill.skill_part_3_id != -1:
            skill_list.append((Skill.objects.get(skill_id=skill.skill_part_3_id)))

        for skill in skill_list:

            multipliers[0] *= skill.hp_mult
            multipliers[1] *= skill.atk_mult
            multipliers[2] *= skill.rcv_mult
            if skill.dmg_reduction != 0:
                shields.append(skill.dmg_reduction)

        for shield in shields:
            shield_calc *= (1 - shield)

        multipliers[3] = round((1 - shield_calc) * 100, 2)
        multipliers[4] = 1 - shield_calc

    else:
        multipliers[0] = skill.hp_mult
        multipliers[1] = skill.atk_mult
        multipliers[2] = skill.rcv_mult
        multipliers[3] = skill.dmg_reduction * 100
        multipliers[4] = skill.dmg_reduction
    return multipliers


def get_evos(evo_list) -> []:
    evos = []
    for evo in evo_list:
        evo_card = Monster.objects.get(card_id=evo)
        if "Alt." not in evo_card.name:
            evos.append(evo_card)
    return evos


def get_dungeons(card_id) -> []:
    dungeon_list = []

    floors = Floor.objects.all()
    for floor in floors:
        drop_data = json.loads(floor.possible_drops)
        for key in drop_data.keys():
            if card_id == int(key):
                dungeon = Dungeon.objects.filter(dungeon_id=floor.dungeon_id)[0]
                if dungeon not in dungeon_list:
                    dungeon_list.append(dungeon)

    return dungeon_list

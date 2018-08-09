from django.shortcuts import render
from .models import Monster, Skill
from .maps import EXPLICIT_TYPE_MAP
import json
import math


def cardView(request, card_id):
    template = 'monster_jp.html'
    monster = Monster.objects.get(cardID=card_id)
    evo_list = monster.evolutions.all()
    monsters = Monster.objects.all()

    # The following set of checks is necessary as some cards do not have leader skills, active skills, or ancestors.
    ancestor = None
    if monster.ancestorID != monster.cardID:
        if monster.ancestorID != 0:
            ancestor = Monster.objects.get(cardID=monster.ancestorID)

    activeskill = None
    leaderskill = None

    if Skill.objects.filter(skillID=monster.activeSkillID).first() is not None:
        activeskill = Skill.objects.get(skillID=monster.activeSkillID)
    if Skill.objects.filter(skillID=monster.leaderSkillID).first() is not None:
        leaderskill = Skill.objects.get(skillID=monster.leaderSkillID)

    multipliers = [1, 1, 1, 0, 0]
    a_multipliers = [1, 1, 1, 0]

    if leaderskill is not None:
        multipliers = getMultipliers(leaderskill)

    if activeskill is not None:
        a_multipliers = getMultipliers(activeskill)

    d_multipliers = [round((item ** 2), 2) for item in multipliers]
    d_multipliers[3] = round((1 - (1 - multipliers[4]) * (1 - multipliers[4])) * 100, 2)

    evos = None
    if len(evo_list) > 0:
        evos = getEvos(evo_list)

    evomats = getEvoMats(monster, monsters)
    unevomats = getUnEvoMats(monster, monsters)

    awakenings = json.loads(monster.awakenings)
    sawakenings = json.loads(monster.superAwakenings)

    types = getTypes(monster)

    context = {'activeskill': activeskill, 'leaderskill': leaderskill,
               'monster': monster, 'ancestor': ancestor, "evolutions": evos, "evomats": evomats,
               "unevomats": unevomats, 'awakenings': awakenings, 'sawakenings': sawakenings, 'types': types,
               'lmultipliers': multipliers, 'dmultipliers': d_multipliers, 'amultipliers': a_multipliers}

    return render(request, template, context)


def cardList(request):
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
    template = 'monster_list_jp.html'
    return render(request, template, context)


def activeSkillListView(request):
    skills = Skill.objects.filter(skill_type="active").all()
    context = {'skills': skills}
    template = 'active_skill_list_jp.html'
    return render(request, template, context)


def activeSkillView(request, id):
    skill = Skill.objects.get(skillID=id)
    monsters = Monster.objects.filter(activeSkillID=id)

    context = {'activeskill': skill, "monsters": monsters}
    template = 'active_skill_jp.html'
    return render(request, template, context)


def leaderSkillListView(request):
    skills = Skill.objects.filter(skill_type="leader").all()
    context = {'skills': skills}
    template = 'leader_skill_list_jp.html'
    return render(request, template, context)


def leaderSkillView(request, id):
    skill = Skill.objects.get(skillID=id)
    monsters = Monster.objects.filter(leaderSkillID=id)

    context = {'leaderskill': skill, "monsters": monsters}
    template = 'leader_skill_jp.html'
    return render(request, template, context)


def getEvoMats(monster, monsters):
    evomats = []
    if monster.evomat1 != 0:
        evomats.append(monsters.get(cardID=monster.evomat1))
    if monster.evomat2 != 0:
        evomats.append(monsters.get(cardID=monster.evomat2))
    if monster.evomat3 != 0:
        evomats.append(monsters.get(cardID=monster.evomat3))
    if monster.evomat4 != 0:
        evomats.append(monsters.get(cardID=monster.evomat4))
    if monster.evomat5 != 0:
        evomats.append(monsters.get(cardID=monster.evomat5))
    return evomats


def getUnEvoMats(monster, monsters):
    evomats = []
    if monster.unevomat1 != 0:
        evomats.append(monsters.get(cardID=monster.unevomat1))
    if monster.unevomat2 != 0:
        evomats.append(monsters.get(cardID=monster.unevomat2))
    if monster.unevomat3 != 0:
        evomats.append(monsters.get(cardID=monster.unevomat3))
    if monster.unevomat4 != 0:
        evomats.append(monsters.get(cardID=monster.unevomat4))
    if monster.unevomat5 != 0:
        evomats.append(monsters.get(cardID=monster.unevomat5))
    return evomats


def getTypes(monster) -> []:
    types = [EXPLICIT_TYPE_MAP[int(monster.type1)], EXPLICIT_TYPE_MAP[int(monster.type2)],
             EXPLICIT_TYPE_MAP[int(monster.type3)]]
    return types


def getMultipliers(skill) -> []:
    skill_list = []
    multipliers = [1, 1, 1, 0, 0]
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
        multipliers[3] = round((1 - shield_calc) * 100, 2)
        multipliers[4] = 1 - shield_calc
    else:
        multipliers[0] = skill.hp_mult
        multipliers[1] = skill.atk_mult
        multipliers[2] = skill.rcv_mult
        multipliers[3] = float(skill.dmg_reduction)
        multipliers[4] = float(skill.dmg_reduction)

    return multipliers


def getEvos(evo_list) -> []:
    evos = []
    for evo in evo_list:
        evoCard = Monster.objects.get(cardID=evo.evo)
        if "Alt." not in evoCard.name:
            evos.append(evoCard)
    return evos

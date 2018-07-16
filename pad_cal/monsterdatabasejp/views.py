from django.shortcuts import render
from .models import CardJP, MonsterData
import json


def cardViewJP(request, card_id):
    template = 'monster.html'
    mnstr = MonsterData.objects.get(cardID=card_id)
    card = CardJP.objects.get(monster=mnstr)
    cards = CardJP.objects.all()
    monsters = MonsterData.objects.all()

    # The following set of checks is necessary as some cards do not have leader skills, active skills, or ancestors.
    ancestor = None
    if mnstr.ancestorID != mnstr.cardID:
        if mnstr.ancestorID != 0:
            ancestor = cards.get(monster=MonsterData.objects.get(cardID=mnstr.ancestorID))

    leaderskill = None
    if card.leaderSkill is not None:
        leaderskill = card.leaderSkill.all().first()

    activeskill = None
    if card.activeSkill is not None:
        activeskill = card.activeSkill.all().first()

    evos = None
    if len(mnstr.evolutions.all()) > 0:
        evos = []

        for evo in mnstr.evolutions.all():
            evoCard = cards.get(monster=MonsterData.objects.get(cardID=evo.evo))
            if "Alt." not in evoCard.monster.name:
                evos.append(evoCard)

    evomats = getEvoMats(mnstr, cards, monsters)
    unevomats = getUnEvoMats(mnstr, cards, monsters)

    awakenings = json.loads(mnstr.awakenings)
    sawakenings = json.loads(mnstr.superAwakenings)

    context = {'activeskill': activeskill, 'leaderskill': leaderskill,
               'monster': card.monster, 'ancestor': ancestor, "evolutions": evos, "evomats": evomats,
               "unevomats": unevomats, 'awakenings': awakenings, 'sawakenings': sawakenings}

    return render(request, template, context)


def getEvoMats(monster, cards, monsters):
    evomats = []

    if monster.evomat1 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.evomat1)))
    if monster.evomat2 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.evomat2)))
    if monster.evomat3 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.evomat3)))
    if monster.evomat4 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.evomat4)))
    if monster.evomat5 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.evomat5)))

    return evomats


def getUnEvoMats(monster, cards, monsters):
    evomats = []

    if monster.unevomat1 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.unevomat1)))
    if monster.unevomat2 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.unevomat2)))
    if monster.unevomat3 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.unevomat3)))
    if monster.unevomat4 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.unevomat4)))
    if monster.unevomat5 != 0:
        evomats.append(cards.get(monster=monsters.get(cardID=monster.unevomat5)))

    return evomats


def cardListJP(request):
    rawCards = MonsterData.objects.all()
    cards = []
    cardID = []

    for card in rawCards:
        if "*" not in card.name:
            if "Alt." not in card.name:
                cards.append(card.name)
                cardID.append(card.cardID)

    cardList = zip(cards, cardID)
    context = {'cards': cardList}
    template = 'monsterlist.html'
    return render(request, template, context)
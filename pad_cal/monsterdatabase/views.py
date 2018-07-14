from django.shortcuts import render
from .models import CardNA, MonsterData


# Create your views here.

def cardViewNA(request, card_id):
    template = 'monster.html'
    mnstr = MonsterData.objects.get(cardID=card_id)
    card = CardNA.objects.get(monster=mnstr)

    ancestor = None

    if mnstr.ancestorID != mnstr.cardID:
        if mnstr.ancestorID != 1929 and mnstr.ancestorID != 0:
            ancestor = CardNA.objects.get(monster=MonsterData.objects.get(cardID=mnstr.ancestorID))

    leaderskill = None
    if card.leaderSkill is not None:
        leaderskill = card.leaderSkill.all().first()

    activeskill = None

    if card.activeSkill is not None:
        activeskill = card.activeSkill.all().first()

    evo = None
    if mnstr.nextEvo != 0:
        evoData = MonsterData.objects.get(cardID=mnstr.nextEvo)
        evo = CardNA.objects.get(monster=evoData)

    context = {'activeskill': activeskill, 'leaderskill': leaderskill,
               'monster': card.monster, 'ancestor': ancestor, 'evolution': evo}

    return render(request, template, context)


def cardListNA(request):
    rawCards = CardNA.objects.all()
    cards = []

    for card in rawCards:
        if "*" not in card.monster.name:
            cards.append(card)

    context = {'cards': cards}
    template = 'monsterlist.html'
    return render(request, template, context)

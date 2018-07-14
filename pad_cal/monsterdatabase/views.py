from django.shortcuts import render
from .models import CardNA, MonsterData


# Create your views here.

def cardViewNA(request, card_id):
    template = 'monster.html'
    mnstr = MonsterData.objects.get(cardID=card_id)
    card = CardNA.objects.get(monster=mnstr)

    # The following set of checks is necessary as some cards do not have leader skills, active skills, or ancestors.
    ancestor = None
    if mnstr.ancestorID != mnstr.cardID:
        if mnstr.ancestorID != 0:
            ancestor = CardNA.objects.get(monster=MonsterData.objects.get(cardID=mnstr.ancestorID))

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
            evoCard = CardNA.objects.get(monster=MonsterData.objects.get(cardID=evo.evo))
            if "Alt." not in evoCard.monster.name:
                evos.append(evoCard)

    context = {'activeskill': activeskill, 'leaderskill': leaderskill,
               'monster': card.monster, 'ancestor': ancestor, "evolutions": evos}

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

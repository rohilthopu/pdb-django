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

    context = {'activeskill': card.activeSkill.all()[0], 'leaderskill': card.leaderSkill.all()[0],
               'monster': card.monster, 'ancestor': ancestor}


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

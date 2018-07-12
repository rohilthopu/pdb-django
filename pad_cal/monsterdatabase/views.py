from django.shortcuts import render
from .models import CardNA, MonsterData


# Create your views here.

def cardViewNA(request, card_id):
    template = 'monster.html'
    mnstr = MonsterData.objects.get(cardID=card_id)
    card = CardNA.objects.get(monster=mnstr)
    context = {'activeskill': card.activeSkill.all()[0], 'leaderskill': card.leaderSkill.all()[0], 'monster': card.monster}

    if card.activeSkill is None:
        print("Not working..")

    return render(request, template, context)


def cardListNA(reqest):
    rawCards = CardNA.objects.all()
    cards = []

    for card in rawCards:
        if "*" not in card.monster.name:
            cards.append(card)



    context = {'cards': cards}
    template = 'monsterlist.html'
    return render(reqest, template, context)

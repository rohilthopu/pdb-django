from django.shortcuts import render
from .models import CardNA, MonsterData


# Create your views here.

def cardViewNA(request, card_id):
    template = 'monster.html'
    card = CardNA.objects.get(pk=card_id)
    context = {'card': card}
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

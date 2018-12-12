from django.shortcuts import render
from .models import Dungeon, Floor
import json

def dungeonListView(request):
    template = 'dungeonlist.html'
    context = {'dungeons': Dungeon.objects.all()}
    return render(request, template, context)


def dungeonView(request, d_id):
    template = 'dungeon.html'
    dungeon = Dungeon.objects.get(dungeonID=d_id)
    floors = Floor.objects.filter(dungeonID=d_id)
    context = {'dungeon': dungeon, 'floors': floors}

    # drops = []
    #
    # rarities = []
    #
    # for floor in floors:
    #
    #     allDrops = json.loads(floor.possibleDrops)
    #     drop = []
    #     rarity = []
    #
    #     for d in allDrops.keys():
    #         drop.append(d)
    #         rarity.append(allDrops[d])
    #
    #     drops.append(drop)
    #     rarities.append(rarity)



    return render(request, template, context)

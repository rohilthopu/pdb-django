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

    drops = []

    rarities = []

    floorData = []

    for floor in floors:

        allDrops = json.loads(floor.possibleDrops)

        for drop in allDrops.keys():
            drops.append(drop)
            rarities.append(allDrops[drop])

        dropData = zip(drops, rarities)

        drops = []
        rarities = []

        floorData.append(dropData)

    context = {'dungeon': dungeon, 'floors': floors, 'drops': floorData}

    return render(request, template, context)

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
    for floor in floors:
        dropList = json.loads(floor.possibleDrops)
        drops.append(dropList)

    # modifiers = [json.loads(floor.teamModifiers) for floor in floors]

    floorData = zip(floors, drops)

    context = {'dungeon': dungeon, 'floors': floors, 'drops': floorData}

    return render(request, template, context)

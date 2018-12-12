from django.shortcuts import render
from .models import Dungeon, Floor


def dungeonListView(request):
    template = 'dungeonlist.html'
    context = {'dungeons': Dungeon.objects.all()}
    return render(request, template, context)


def dungeonView(request, d_id):
    template = 'dungeon.html'
    dungeon = Dungeon.objects.get(dungeonID=d_id)
    floors = Floor.objects.filter(dungeonID=d_id)
    context = {'dungeon': dungeon, 'floors': floors}

    return render(request, template, context)
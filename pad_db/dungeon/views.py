from django.shortcuts import render
from .models import Dungeon

def DungeonView(request):
    template = 'dungeonlist.html'

    context = {'dungeons': Dungeon.objects.all()}

    return render(request, template, context)


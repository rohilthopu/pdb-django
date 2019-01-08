from django.shortcuts import render
from .models import GuerrillaDungeon
from dungeon.models import Dungeon
from datetime import date
from time import time


# Create your views here.

def DungeonView(request):
    template = 'home.html'
    naDungeons = GuerrillaDungeon.objects.filter(server="NA").order_by('group').all()
    jpDungeons = GuerrillaDungeon.objects.filter(server="JP").order_by('group').all()
    dateT = date.today()
    timeNow = time()
    naActives = []
    jpActives = []

    for d in naDungeons:
        if d.startSecs <= timeNow <= d.endSecs:
            naActives.append("Active")
        elif timeNow < d.startSecs:
            naActives.append("Upcoming")
        else:
            naActives.append("Ended")

    for d in jpDungeons:
        if d.startSecs <= timeNow <= d.endSecs:
            jpActives.append("Active")
        elif timeNow < d.startSecs:
            jpActives.append("Upcoming")
        else:
            jpActives.append("Ended")

    naDungeonID = []

    for dungeon in naDungeons:
        d_id = Dungeon.objects.filter(name=dungeon.name)[0].dungeonID
        naDungeonID.append(d_id)

    na = zip(naDungeons, naActives, naDungeonID)
    jp = zip(jpDungeons, jpActives)

    context = {'date': dateT, 'na': na, 'jp': jp}

    return render(request, template, context)

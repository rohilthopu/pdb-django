from django.shortcuts import render
from .models import GuerrillaDungeon
from datetime import date
from time import time


# Create your views here.

def DungeonView(request):
    template = 'home.html'
    na_dungeons = GuerrillaDungeon.objects.filter(server="NA").order_by('group').all()
    jp_dungeons = GuerrillaDungeon.objects.filter(server="JP").order_by('group').all()
    date_t = date.today()
    time_now = time()
    na_actives = []
    jp_actives = []

    for d in na_dungeons:
        if d.start_secs <= time_now <= d.end_secs:
            na_actives.append("Active")
        elif time_now < d.start_secs:
            na_actives.append("Upcoming")
        else:
            na_actives.append("Ended")

    for d in jp_dungeons:
        if d.start_secs <= time_now <= d.end_secs:
            jp_actives.append("Active")
        elif time_now < d.start_secs:
            jp_actives.append("Upcoming")
        else:
            jp_actives.append("Ended")

    # naDungeonID = []
    #
    # for dungeons in na_dungeons:
    #     d_id = Dungeon.objects.filter(name=dungeons.name)[0].dungeonID
    #     naDungeonID.append(d_id)

    na = zip(na_dungeons, na_actives)
    jp = zip(jp_dungeons, jp_actives)

    context = {'date': date_t, 'na': na, 'jp': jp}

    return render(request, template, context)

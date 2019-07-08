from django.shortcuts import render
from .models import GuerrillaDungeon
from datetime import date


def guerrilla_view(request):
    template = 'home.html'
    na_dungeons = GuerrillaDungeon.objects.filter(status='Active').order_by('server', 'group').reverse()
    jp_dungeons = GuerrillaDungeon.objects.filter(status='Upcoming').order_by('server', 'group').reverse()
    date_t = date.today()
    context = {'date': date_t, 'na_dungeons': na_dungeons, 'jp_dungeons': jp_dungeons}

    return render(request, template, context)

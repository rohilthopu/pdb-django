from django.shortcuts import render
from .models import GuerrillaDungeon
from datetime import date
# Create your views here.

def DungeonView(request):

    template = 'home.html'
    na = GuerrillaDungeon.objects.filter(server="NA").order_by('group').all()
    jp = GuerrillaDungeon.objects.filter(server="JP").order_by('group').all()
    dateT = date.today()

    context = {'date': dateT, 'na': na, 'jp': jp}


    return render(request, template, context)

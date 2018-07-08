from datetime import date
from django.shortcuts import render, redirect

from .forms import DungeonLink, DailyDungeonSelector
from .models import Dungeon, DungeonToday, Monster, Skill
from .parse import parse
from celery import task


# Create your views here.


def homeView(request):
    template = 'home.html'

    if request.method == 'POST':
        form = DailyDungeonSelector(request.POST)
        if (form.is_valid()):
            # verify that it doesnt already exist
            data = form.cleaned_data['dungeon']
            todaysList = DungeonToday.objects.filter(listingDate=date.today()).first()
            addDungeon = Dungeon.objects.get(jpnTitle=data.jpnTitle)
            if todaysList is not None:
                todaysList = DungeonToday.objects.get(listingDate=date.today())
                if addDungeon not in todaysList.dungeons.all():
                    todaysList.dungeons.add(addDungeon)
                    todaysList.save()
                    return redirect('/')

    dungeonList = DungeonToday.objects.filter(listingDate=date.today()).first()
    if dungeonList is None:
        todaysList = DungeonToday()
        todaysList.save()
        dungeonList = todaysList
    form = DailyDungeonSelector()

    context = {'dungeons': dungeonList.dungeons.all(), 'form': form, 'date': dungeonList.listingDate}
    return render(request, template, context)


def addDungeonView(request):
    template = 'addDungeon.html'
    source = Dungeon.objects.all()
    form = DungeonLink()

    context = {'dungeons': source, 'form': form}

    if request.method == 'POST':
        form = DungeonLink(request.POST)
        if (form.is_valid()):
            # verify that it doesnt already exist
            data = form.cleaned_data
            exists = False

            link = data.get('dungeonLink')

            if 'mission' in link:
                for item in source:
                    if item.dungeonLink.rsplit('=', 1)[1].lower() in link.lower():
                        exists = True
                if (not exists):
                    dungeon = Dungeon()
                    dungeon.save()
                    dungeon.dungeonLink = link
                    parse(link, dungeon)
                    return redirect('/add/')
                else:
                    return redirect('/add/')
    return render(request, template, context)


def allDungeons(request):
    dungeons = Dungeon.objects.order_by('altTitle').all()
    template = 'allDungeons.html'
    context = {'dungeons': dungeons}
    return render(request, template, context)


def allEncounters(request):
    monsters = Monster.objects.order_by('name').all()
    template = 'allEncounters.html'
    context = {'monsters': monsters}
    return render(request, template, context)


def allSkills(request):
    skills = Skill.objects.order_by('name').all()
    template = 'allSkills.html'
    context = {'skills': skills}
    return render(request, template, context)


def dungeonView(request, d_id):
    dungeon = Dungeon.objects.get(pk=d_id)
    template = 'dungeondetail.html'

    return render(request, template, {'dungeon': dungeon})


def monsterView(request, m_name):
    monster = Monster.objects.get(name=m_name)
    template = 'monsterdetail.html'

    return render(request, template, {'monster': monster})

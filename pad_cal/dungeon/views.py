from django.shortcuts import render, redirect
from .models import Dungeon, DungeonToday, Monster
from .forms import DungeonLink, DailyDungeonSelector
from bs4 import BeautifulSoup as bs
import urllib
from datetime import date

# Create your views here.

parsedDungeon = {}


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
        dungeonList = DungeonToday.objects.get(listingDate=date.today())
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
                    if item.dungeonLink.rsplit('/', 1)[1].lower() in link.lower():
                        exists = True
                if (not exists):
                    parsedDungeon['dungeonLink'] = link
                    dungeon = Dungeon()
                    dungeon.save()

                    parse(link, dungeon)

                    dungeon.jpnTitle=parsedDungeon['jpnTitle']
                    dungeon.altTitle=parsedDungeon['altTitle']
                    dungeon.altTitle2=parsedDungeon['altTitle2']
                    dungeon.stamina=parsedDungeon['stamina']
                    dungeon.battles=parsedDungeon['battles']
                    dungeon.dungeonLink=parsedDungeon['dungeonLink']
                    dungeon.dungeonType=parsedDungeon['dungeonType']
                    dungeon.save()
                    return redirect('/add/')
                else:
                    return redirect('/add/')
    return render(request, template, context)


def parse(link, dungeon):
    site = urllib.request.urlopen(link)
    soup = bs(site, 'lxml')
    parse_titles(soup)
    parse_dungeon(soup)
    parse_encounters(soup, dungeon)


def parse_titles(soup):
    # The title of the dungeon
    title = soup.body.find(class_='name').get_text().strip()
    # Japanese Title
    titlej = soup.body.find(class_='jap').get_text()
    # Alternate Name
    alt_title = soup.body.find(class_='title value-end nowrap').get_text().strip()

    parsedDungeon['jpnTitle'] = titlej
    parsedDungeon['altTitle'] = alt_title
    parsedDungeon['altTitle2'] = title


def parse_dungeon(soup):
    # The type of Dungeon (normal, special,etc)
    dungeon_type = soup.body.find(class_='title value-end').get_text().strip()
    type_split = ''.join([line.strip() for line in dungeon_type])

    stats = soup.body.find_all(class_='title')
    stat_vals = soup.body.find_all(class_="value-end")

    # Stamina val
    stam = soup.body.find(class_='blue').text

    # Num of Battles
    battles = soup.body.find(class_='green').text

    # Correct dungeon typing becuase fuck it
    if type_split == "SpecialDungeon":
        type_split = "Special Dungeon"
    elif type_split == "NormalDungeon":
        type_split = "Normal Dungeon"

    parsedDungeon['dungeonType'] = type_split
    parsedDungeon['stamina'] = stam
    parsedDungeon['battles'] = battles


def parse_encounters(soup, dungeon):

    # Battle encounters
    encounters = soup.body.find(id="tabledrop").find_all("tr")
    floor = 0
    # This method counts floors because I need to know how many encounter sets there are to know
    # how many times to repeat the first set.
    for item in encounters:
        table1 = item.find_all("td")
        for dat in table1:
            attrs = dat.attrs
            if 'class' in attrs:
                if 'floorcontainer' in attrs['class']:
                    floor += 1

    num_repetitions = int(soup.body.find(class_='green').text) - floor + 1
    num_rep_temp = num_repetitions
    floor = 1
    for item in encounters:
        table1 = item.find_all("td")
        for dat in table1:
            attrs = dat.attrs
            if 'class' in attrs:
                if 'floorcontainer' in attrs['class']:
                    if num_rep_temp > 1:
                        # print("Encounter Set", floor, ", Repeated", num_repetitions, " times.")
                        floor += num_repetitions
                        num_rep_temp = 0
                    else:
                        # print("Encounter Set", floor)
                        floor += 1



                cardname = dat.find(class_='cardname')
                if cardname is not None:
                    # print("\t", cardname.text)

                    monster = Monster()
                    # get the monster name first
                    monster.name = cardname.text

                    health = item.find(class_='nc bossHp')
                    if health is not None:
                        monster.hp = health.text
                        # print('\t\tHP :', health.text)
                    else:
                        health = item.find(class_='nc')
                        if health is not None:
                            monster.hp = health.text
                            # print('\t\tHP :', health.text)
                    attack = item.find(class_='blue nc bossAtk')
                    if attack is not None:
                        monster.atk = attack.text
                        # print("\t\tAtk :", attack.text)
                    else:
                        attack = item.find(class_='blue nc')
                        if attack is not None:
                            # print('\t\tAtk :', attack.text)
                            monster.atk = attack.text
                    defense = item.find(class_='green nc')
                    if defense is not None:
                        # print('\t\tDEF :', defense.text)
                        monster.defense = defense.text

                    # memo = item.find(class_='mmemodetail').find_all('a')
                    # for thing in memo:
                    #     href = thing['href']
                    #     if 'enemyskill' in href:
                    #         # print('\t\t', href)
                    #         parse_skill(href)

                    monster.save()
                    dungeon.monsters.add(monster)


def parse_skill(href):
    base_link = "http://www.puzzledragonx.com/en/"
    skill_link = base_link + href
    site = urllib.request.urlopen(skill_link)
    ss = bs(site, 'lxml')
    skill = ss.find_all(class_='value-end')
    print('\t\tSkill Name :', skill[0].text, ",", skill[2].text)
    print('\t\t\tSkill Effect :', skill[1].text)

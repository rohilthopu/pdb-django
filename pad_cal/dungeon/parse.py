import urllib
from bs4 import BeautifulSoup as bs
from .models import Skill, Monster, Dungeon


def parse(link, dungeon):
    site = urllib.request.urlopen(link)
    soup = bs(site, 'lxml')
    parse_titles(soup, dungeon)
    parse_dungeon(soup, dungeon)
    parse_encounters(soup, dungeon)


def parse_titles(soup, dungeon):
    # The title of the dungeon
    title = soup.body.find(class_='name').get_text().strip()
    # Japanese Title
    titlej = soup.body.find(class_='jap').get_text()
    # Alternate Name
    alt_title = soup.body.find(class_='title value-end nowrap').get_text().strip()

    dungeon.jpnTitle = titlej
    dungeon.altTitle = alt_title
    dungeon.altTitle2 = title


def parse_dungeon(soup, dungeon):
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

    dungeon.dungeonType = type_split
    dungeon.stamina = stam
    dungeon.battles = battles


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
                        floor += num_repetitions
                        num_rep_temp = 0
                        dungeon.repeat = num_repetitions
                    else:
                        floor += 1

                cardname = dat.find(class_='cardname')
                if cardname is not None:
                    # print("\t", cardname.text)

                    if Monster.objects.filter(name=cardname.text).first() is None:

                        monster = Monster()
                        monster.save()
                        # get the monster name first
                        monster.name = cardname.text

                        health = item.find(class_='nc bossHp')
                        if health is not None:
                            monster.hp = health.text
                        else:
                            health = item.find(class_='nc')
                            if health is not None:
                                monster.hp = health.text
                        attack = item.find(class_='blue nc bossAtk')
                        if attack is not None:
                            monster.atk = attack.text
                        else:
                            attack = item.find(class_='blue nc')
                            if attack is not None:
                                monster.atk = attack.text
                        defense = item.find(class_='green nc')
                        if defense is not None:
                            monster.defense = defense.text

                        memo = item.find(class_='mmemodetail').find_all('a')
                        for thing in memo:
                            href = thing['href']
                            if 'enemyskill' in href:
                                parse_skill(href, monster)

                        monster.save()
                        dungeon.monsters.add(monster)
                    else:
                        monster = Monster.objects.filter(name=cardname.text)
                        dungeon.monsters.add(monster)


def parse_skill(href, monster):
    base_link = "http://www.puzzledragonx.com/en/"
    skill_link = base_link + href
    site = urllib.request.urlopen(skill_link)
    ss = bs(site, 'lxml')
    skill = ss.find_all(class_='value-end')

    skill_actual = Skill()
    skill_actual.name = skill[0].text
    skill_actual.altName = skill_actual[2].text
    skill_actual.effect = skill[1].text
    skill_actual.save()
    monster.skills.add(skill_actual)

    # print('\t\tSkill Name :', skill[0].text, ",", skill[2].text)
    # print('\t\t\tSkill Effect :', skill[1].text)
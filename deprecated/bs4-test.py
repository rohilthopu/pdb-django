import urllib

from bs4 import BeautifulSoup as bs

import lxml

links = ["http://www.puzzledragonx.com/en/mission.asp?m=3047", "http://www.puzzledragonx.com/en/mission.asp?m=2207",
         "http://www.puzzledragonx.com/en/mission.asp?m=681", "http://www.puzzledragonx.com/en/mission.asp?m=3121"]
base_link = "http://www.puzzledragonx.com/en/"


def parse(link):
    site = urllib.request.urlopen(link)
    soup = bs(site, 'lxml')
    parse_titles(soup)
    parse_dungeon(soup)
    parse_encounters(soup)


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

    print("Dungeon Type :", type_split)
    print("Stamina :", stam)
    print("Battles :", battles)


def parse_titles(soup):
    # The title of the dungeon
    title = soup.body.find(class_='name').get_text().strip()
    # Japanese Title
    titlej = soup.body.find(class_='jap').get_text()
    # Alternate Name
    alt_title = soup.body.find(class_='title value-end nowrap').get_text().strip()
    print("JPN Title :", titlej)
    print("Alt Titles :", alt_title, ",", title)


def parse_encounters(soup):
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
                        print("Encounter Set", floor, ", Repeated", num_repetitions, " times.")
                        floor += num_repetitions
                        num_rep_temp = 0
                    else:
                        print("Encounter Set", floor)
                        floor += 1

                cardname = dat.find(class_='cardname')
                if cardname is not None:
                    print("\t", cardname.text)
                    health = item.find(class_='nc bossHp')
                    if health is not None:
                        print('\t\tHP :', health.text)
                    else:
                        health = item.find(class_='nc')
                        if health is not None:
                            print('\t\tHP :', health.text)
                    attack = item.find(class_='blue nc bossAtk')
                    if attack is not None:
                        print("\t\tAtk :", attack.text)
                    else:
                        attack = item.find(class_='blue nc')
                        if attack is not None:
                            print('\t\tAtk :', attack.text)
                    defense = item.find(class_='green nc')
                    if defense is not None:
                        print('\t\tDEF :', defense.text)

                    memo = item.find(class_='mmemodetail').find_all('a')
                    for thing in memo:
                        href = thing['href']
                        if 'enemyskill' in href:
                            # print('\t\t', href)
                            parse_skill(href)
def parse_skill(href):
    skill_link = base_link + href
    site = urllib.request.urlopen(skill_link)
    ss = bs(site, 'lxml')
    skill = ss.find_all(class_='value-end')
    print('\t\tSkill Name :', skill[0].text, ",",skill[2].text)
    print('\t\t\tSkill Effect :', skill[1].text)

# for link in links:
#     parse(link)
#     print()

parse(links[3])

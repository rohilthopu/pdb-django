import urllib

from bs4 import BeautifulSoup as bs
import html5lib

links = ["http://www.puzzledragonx.com/en/mission.asp?m=3047", "http://www.puzzledragonx.com/en/mission.asp?m=2207",
         "http://www.puzzledragonx.com/en/mission.asp?m=681", "http://www.puzzledragonx.com/en/mission.asp?m=3121"]
base_link = "http://www.puzzledragonx.com/en/mission.asp?m="


def parse(link):
    site = urllib.request.urlopen(link)
    soup = bs(site, 'html5lib')

    # print(soup.body.prettify())

    # The title of the dungeon
    title = soup.body.find(class_='name').get_text().strip()

    # Japanese Title
    titlej = soup.body.find(class_='jap').get_text()

    # Alternate Name
    alt_title = soup.body.find(class_='title value-end nowrap').get_text().strip()

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

    print("JPN Title :", titlej)
    # print("NA Title :", alt_title)
    print("Alt Titles :", alt_title, ",", title)
    print("Dungeon Type :", type_split)
    print("Stamina :", stam)
    print("Battles :", battles)

    # Battle encounters
    encounters = soup.body.find(id="tabledrop").find_all("tr")

    floor = 1

    for item in encounters:
        table1 = item.find_all("td")

        for dat in table1:

            attrs = dat.attrs

            if 'class' in attrs:
                if 'floorcontainer' in attrs['class']:
                    print('Encounter Set', floor)
                    floor += 1

                cardname = dat.find(class_='cardname')
                if cardname is not None:
                    print("\t",cardname.text)

#
for link in links:
    parse(link)
    print()

# parse(links[2])

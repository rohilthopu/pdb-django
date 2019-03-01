import json
import time
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pad_db.settings")
django.setup()

from pad_db.monsterdatabase.models import Monster, Evolution
from pad_db.dataversions.models import Version
from maps import TYPE_MAP, AWAKENING_MAP


def makeMonster(rawCard):
    monster = Monster()
    monster.save()
    monster.activeSkillID = rawCard['active_skill_id']
    monster.ancestorID = rawCard['ancestor_id']
    monster.attributeID = rawCard['attr_id']

    awakenings = []
    awakenings_raw = []
    for a in rawCard['awakenings']:
        awakenings_raw.append(int(a))
        awakening = AWAKENING_MAP[a]
        if awakening != "":
            awakenings.append(awakening)

    jsonDump = json.dumps(awakenings)
    jsonDump2 = json.dumps(awakenings_raw)

    monster.awakenings = jsonDump
    monster.awakenings_raw = jsonDump2
    monster.baseID = rawCard['base_id']
    monster.cardID = rawCard['card_id']
    monster.cost = rawCard['cost']
    monster.inheritable = "Yes" if rawCard['inheritable'] else "No"
    monster.isCollab = "Yes" if rawCard['is_collab'] else "No"
    monster.isReleased = "Yes" if rawCard['released_status'] else "No"
    monster.isUlt = rawCard['is_ult']
    monster.leaderSkillID = rawCard['leader_skill_id']
    monster.maxATK = rawCard['max_atk']
    monster.maxHP = rawCard['max_hp']
    monster.maxLevel = rawCard['max_level']
    monster.maxRCV = rawCard['max_rcv']
    monster.minATK = rawCard['min_atk']
    monster.minHP = rawCard['min_hp']
    monster.minRCV = rawCard['min_rcv']
    monster.maxXP = rawCard['xp_max']

    monster.name = rawCard['name']
    if monster.cardID >= 100000:
        if "alt." not in rawCard['name'].lower():
            name = rawCard['name']
            altname = "Alt. " + name
            monster.name = altname

    monster.rarity = rawCard['rarity']
    monster.subAttributeID = rawCard['sub_attr_id']
    monster.evomat1 = rawCard['evo_mat_id_1']
    monster.evomat2 = rawCard['evo_mat_id_2']
    monster.evomat3 = rawCard['evo_mat_id_3']
    monster.evomat4 = rawCard['evo_mat_id_4']
    monster.evomat5 = rawCard['evo_mat_id_5']

    if monster.ancestorID != 0:
        monster.unevomat1 = rawCard['un_evo_mat_1']
        monster.unevomat2 = rawCard['un_evo_mat_2']
        monster.unevomat3 = rawCard['un_evo_mat_3']
        monster.unevomat4 = rawCard['un_evo_mat_4']
        monster.unevomat5 = rawCard['un_evo_mat_5']

    monster.hp99 = monster.maxHP + 990
    monster.atk99 = monster.maxATK + 495
    monster.rcv99 = monster.maxRCV + 495

    monster.type1 = TYPE_MAP[rawCard['type_1_id']]
    monster.type2 = TYPE_MAP[rawCard['type_2_id']]
    monster.type3 = TYPE_MAP[rawCard['type_3_id']]

    sawakenings = []
    sawakenings_raw = []
    for sa in rawCard['super_awakenings']:
        awakening = AWAKENING_MAP[sa]
        sawakenings_raw.append(int(sa))
        if awakening != "":
            sawakenings.append(awakening)
    sadump = json.dumps(sawakenings)
    monster.superAwakenings = sadump
    monster.superAwakenings_raw = json.dumps(sawakenings_raw)

    monster.sellMP = rawCard['sell_mp']
    monster.sellCoin = rawCard['sell_price_at_lvl_10']

    enemy_skills = []

    for skill in rawCard['enemy_skill_refs']:
        enemy_skills.append(skill['enemy_skill_id'])

    monster.enemy_skills = json.dumps(enemy_skills)

    monster.save()


def update_monsters():
    m = Monster.objects.all()
    prevSize = m.count()
    m.delete()
    Evolution.objects.all().delete()

    with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/na_cards.json'), 'r') as jsonPull:

        print()
        print('Starting monster database update')

        # Pull the new data, because with PAD, things often get buffs/changes often

        cards = json.load(jsonPull)
        start_time = time.time()
        print()
        print('Adding NA cards')

        for card in cards:

            released = card['card']['released_status']

            cardName = card['card']['name']
            if released and cardName is not '' and '*' not in cardName:

                rawCard = card['card']

                if not isinstance(rawCard, type(None)):
                    makeMonster(rawCard)

    monsters = Monster.objects.all()

    # merge in JP monsters
    with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/jp_cards.json'), 'r') as jsonPull:
        jsonData = json.load(jsonPull)

        print('Merging in JP mards')
        print()
        for card in jsonData:
            name = card['card']['name']
            if name != '':
                rawCard = card['card']
                cardID = rawCard['card_id']
                if not monsters.filter(cardID=cardID).exists():
                    makeMonster(rawCard)

    monsters = Monster.objects.all()

    print('Monster list update complete')
    print()
    print("Building evolution list")
    print()

    for monster in monsters:
        if monster.ancestorID != monster.cardID:
            if monster.ancestorID != 0:
                ancestor = monsters.get(cardID=monster.ancestorID)
                evo = Evolution(evo=monster.cardID)
                evo.save()
                ancestor.evolutions.add(evo)
                ancestor.save()

    for monster in monsters:

        parsedEvos = monster.evolutions.all()
        evos = []
        for evo in parsedEvos:
            evos.append(evo.evo)
        monster.evos_raw = json.dumps(evos)
        monster.save()

    end_time = time.time()

    print('Database update complete')

    print()
    print("Updating version")

    ver = Version.objects.all()

    if len(ver) == 0:
        v = Version()
        v.dungeon = 1
        v.monster = 1
        v.skill = 1
        v.save()
    else:
        v = ver.first()
        if prevSize < monsters.count():
            v.monster += 1
        v.save()

    print("Elapsed time :", end_time - start_time)
    print()

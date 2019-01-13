from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import Monster, Evolution
import requests
import json
import time

from .maps import TYPE_MAP, AWAKENING_MAP


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        Monster.objects.all().delete()
        Evolution.objects.all().delete()

        monsters = Monster.objects.all()

        print()
        self.stdout.write(self.style.SUCCESS('Starting NA MONSTER DB update.'))

        # Pull the new data, because with PAD, things often get buffs/changes often
        monsterLink = "https://storage.googleapis.com/mirubot/paddata/processed/na_cards.json"

        loadSite = requests.get(monsterLink)
        cards = json.loads(loadSite.text)
        start_time = time.time()
        print()
        self.stdout.write(self.style.SUCCESS('Adding new NA Cards.'))

        newMonsters = []

        for card in cards:

            if '?' not in card['card']['name']:

                rawCard = card['card']

                if not isinstance(rawCard, type(None)):

                    # if not monsters.filter(cardID=rawCard['card_id']).exists():

                        # print("\t\tAdding new entry for", rawCard['name'])

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


                        monster.save()

                        newMonsters.append(monster)

        self.stdout.write(self.style.SUCCESS('NA Monster List Updated.'))
        print()
        self.stdout.write(self.style.SUCCESS('Updating forward evolutions.'))
        print()

        for monster in newMonsters:
            if monster.ancestorID != monster.cardID:
                if monster.ancestorID != 0:
                    ancestor = monsters.get(cardID=monster.ancestorID)
                    evo = Evolution(evo=monster.cardID)
                    evo.save()
                    ancestor.evolutions.add(evo)


        for monster in newMonsters:
            parsedEvos = monster.evolutions.all()
            evos = []
            for evo in parsedEvos:
                evos.append(evo.evo)

            monster.evos_raw = json.dumps(evos)
            monster.save()

        end_time = time.time()

        self.stdout.write(self.style.SUCCESS('NA update complete.'))

        print("Elapsed time :", end_time - start_time)
        print()

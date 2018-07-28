from django.core.management.base import BaseCommand, CommandError
from monsterdatabasejp.models import CardJP, ActiveSkill, LeaderSkill, MonsterData, Evolution
import requests
import json
import time

from .maps import TYPE_MAP, AWAKENING_MAP


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Starting JP MONSTER DB update.'))

        start_time = time.time()

        # Pull the new data, because with PAD, things often get buffs/changes often
        monsterLink = "https://storage.googleapis.com/mirubot/paddata/processed/jp_cards.json"

        loadSite = requests.get(monsterLink)
        cards = json.loads(loadSite.text)
        print()
        self.stdout.write(self.style.SUCCESS('Adding new JP Cards.'))

        for card in cards:

            if '?' not in card['card']['name']:
                monsterCard = CardJP()
                monsterCard.save()
                rawCard = card['card']

                if not isinstance(rawCard, type(None)):
                    monster = MonsterData()
                    monster.save()
                    monster.activeSkillID = rawCard['active_skill_id']
                    monster.ancestorID = rawCard['ancestor_id']
                    monster.attributeID = rawCard['attr_id']

                    awakenings = []
                    for a in rawCard['awakenings']:
                        awakening = AWAKENING_MAP[a]
                        if awakening != "":
                            awakenings.append(awakening)

                    jsonDump = json.dumps(awakenings)
                    monster.awakenings = jsonDump
                    monster.baseID = rawCard['base_id']
                    monster.cardID = rawCard['card_id']
                    monster.cost = rawCard['cost']
                    monster.furigana = rawCard['furigana']
                    monster.inheritable = rawCard['inheritable']
                    monster.isCollab = rawCard['is_collab']
                    monster.isReleased = rawCard['released_status']
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
                    for sa in rawCard['super_awakenings']:
                        awakening = AWAKENING_MAP[sa]
                        if awakening != "":
                            sawakenings.append(awakening)
                    sadump = json.dumps(sawakenings)
                    monster.superAwakenings = sadump

                    monster.save()
                    monsterCard.monster = monster

                rawActiveSkill = card['active_skill']

                if not isinstance(rawActiveSkill, type(None)):

                    # Check if a skill with the same ID already exists.
                    # This is to deal with the situations where a skill has Name and Description of something
                    # like "*****", because these are still valid.
                    skillExists = ActiveSkill.objects.filter(skillID=rawActiveSkill['skill_id']).first()

                    if skillExists is None:
                        activeSkill = ActiveSkill()
                        activeSkill.name = rawActiveSkill['name']
                        activeSkill.description = rawActiveSkill['clean_description']
                        activeSkill.skillID = rawActiveSkill['skill_id']
                        activeSkill.skillType = rawActiveSkill['skill_type']
                        activeSkill.levels = rawActiveSkill['levels']
                        activeSkill.maxTurns = rawActiveSkill['turn_max']
                        activeSkill.minTurns = rawActiveSkill['turn_min']

                        activeSkill.save()
                        monsterCard.activeSkill.add(activeSkill)

                    else:
                        monsterCard.activeSkill.add(ActiveSkill.objects.get(skillID=rawActiveSkill['skill_id']))

                # Next we need to collect the Cards leader skill

                rawLeaderSkill = card['leader_skill']
                if not isinstance(rawLeaderSkill, type(None)):
                    # Similarly to Active Skills, we need to consider null skills
                    skillExists = LeaderSkill.objects.filter(skillID=rawLeaderSkill['skill_id']).first()

                    if skillExists is None:
                        leaderSkill = LeaderSkill()

                        leaderSkill.name = rawLeaderSkill['name']
                        leaderSkill.description = rawLeaderSkill['clean_description']
                        leaderSkill.skillID = rawLeaderSkill['skill_id']
                        leaderSkill.skillType = rawLeaderSkill['skill_type']

                        leaderSkill.save()
                        monsterCard.leaderSkill.add(leaderSkill)
                    else:
                        monsterCard.leaderSkill.add(LeaderSkill.objects.get(skillID=rawLeaderSkill['skill_id']))

                monsterCard.save()

        self.stdout.write(self.style.SUCCESS('JP Monster List Updated.'))
        print()
        self.stdout.write(self.style.SUCCESS('Updating forward evolutions.'))

        monsters = MonsterData.objects.all()
        for monster in monsters:
            if monster.ancestorID != monster.cardID:
                if monster.ancestorID != 0:
                    ancestor = monsters.get(cardID=monster.ancestorID)
                    evo = Evolution(evo=monster.cardID)
                    evo.save()
                    ancestor.evolutions.add(evo)

        end_time = time.time()

        self.stdout.write(self.style.SUCCESS('JP update complete.'))

        print("Elapsed time :", end_time - start_time)

from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import CardNA, ActiveSkill, LeaderSkill, MonsterData, Evolution
import requests
import json
import time


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        start_time = time.time()

        print("Clearing DB")
        print()

        # Wipe the current DB to get up to date data
        cardData = CardNA.objects.all()
        activeSkillData = ActiveSkill.objects.all()
        leaderSkillData = LeaderSkill.objects.all()
        monsterData = MonsterData.objects.all()
        evolutions = Evolution.objects.all()

        if len(cardData) > 0:
            print("Clearing Cards...")
            for card in cardData:
                card.delete()
            print("Clearing Active Skills...")
            for skill in activeSkillData:
                skill.delete()
            print("Clearing Leader Skills...")
            for skill in leaderSkillData:
                skill.delete()
                print("Clearing Evolutions...")
            for evo in evolutions:
                evo.delete()
            print("Clearing Monsters...")
            for monster in monsterData:
                monster.delete()

            print()
            self.stdout.write(self.style.SUCCESS('Current DB succesfully erased.'))

        else:
            self.stdout.write(self.style.SUCCESS('Current DB is empty.'))

        print()
        self.stdout.write(self.style.SUCCESS('Starting DB update.'))

        # Pull the new data, because with PAD, things often get buffs/changes often
        monsterLink = "https://storage.googleapis.com/mirubot/paddata/processed/na_cards.json"

        loadSite = requests.get(monsterLink)
        cards = json.loads(loadSite.text)
        print()
        self.stdout.write(self.style.SUCCESS('Adding new Cards.'))

        for card in cards:

            if '?' not in card['card']['name']:
                monsterCard = CardNA()
                monsterCard.save()
                rawCard = card['card']

                if not isinstance(rawCard, type(None)):
                    monster = MonsterData()

                    monster.activeSkillID = rawCard['active_skill_id']
                    monster.ancestorID = rawCard['ancestor_id']
                    monster.attributeID = rawCard['attr_id']
                    monster.baseID = rawCard['base_id']
                    monster.cardID = rawCard['card_id']
                    monster.cost = rawCard['cost']
                    monster.inheritable = rawCard['inheritable']
                    monster.isCollab = rawCard['is_collab']
                    monster.isReleased = rawCard['is_released']
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
                    monster.rarity = rawCard['rarity']
                    monster.subAttributeID = rawCard['sub_attr_id']

                    monster.hp99 = monster.maxHP + 990
                    monster.atk99 = monster.maxATK + 495
                    monster.rcv99 = monster.maxRCV + 495

                    monster.save()
                    monsterCard.monster = monster

                # print("Processing card", rawCard['name'])

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

        self.stdout.write(self.style.SUCCESS('Monster List Updated.'))
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

        self.stdout.write(self.style.SUCCESS('Update complete.'))

        print("Elapsed time :", end_time - start_time)

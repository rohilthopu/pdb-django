from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import CardNA, ActiveSkill, LeaderSkill
import requests
import json


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        # Wipe the current DB to get up to date data
        currentDB = CardNA.objects.all()

        if len(currentDB) > 0:
            for card in currentDB:
                print("Deleting", card.activeSkill.name)
                card.delete()

            self.stdout.write(self.style.SUCCESS('Current DB succesfully erased.'))

        else:
            self.stdout.write(self.style.SUCCESS('Current DB is empty.'))


        self.stdout.write(self.style.SUCCESS('Starting DB update.'))

        # Pull the new data, because with PAD, things often get buffs/changes often
        monsterLink = "https://storage.googleapis.com/mirubot/paddata/processed/na_cards.json"

        loadSite = requests.get(monsterLink)
        cards = json.loads(loadSite.text)

        for card in cards:

            if '?' not in card['card']['name']:
                monsterCard = CardNA()

                self.stdout.write(self.style.SUCCESS('Adding new Cards.'))

                rawCard = card['card']

                print("Processing card", rawCard['name'])

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
                        monsterCard.activeSkill = activeSkill
                        monsterCard.save()

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
                        monsterCard.leaderSkill = leaderSkill
                        monsterCard.save()




        self.stdout.write(self.style.SUCCESS('Monster List Updated.'))

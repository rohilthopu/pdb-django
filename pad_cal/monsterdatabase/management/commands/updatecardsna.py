from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import CardNA, ActiveSkill
import requests
import json

class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        monsterLink = "https://storage.googleapis.com/mirubot/paddata/processed/na_cards.json"

        loadSite = requests.get(monsterLink)
        cards = json.loads(loadSite.text)

        for card in cards:

            if '?' or '*' not in card['card']['name']:
                monsterCard = CardNA()

                rawActiveSkill = card['active_skill']


                if not isinstance(rawActiveSkill['name'], type(None)):
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






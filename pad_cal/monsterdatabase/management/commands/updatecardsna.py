from django.core.management.base import BaseCommand, CommandError
from pad_cal.monsterdatabase.models import CardNA
import requests
import json

class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        monsterLink = "https://storage.googleapis.com/mirubot/paddata/processed/na_cards.json"

        loadSite = requests.get(monsterLink)
        cards = json.loads(loadSite.text)

        for card in cards:
            card = CardNA()
            card.save()

            activeSkill = card['active_skill']

            card.activeSkill.name = activeSkill['name']
            card.activeSkill.description = activeSkill['clean_description']
            card.activeSkill.skillID = activeSkill['skill_id']
            card.activeSkill.skillType = activeSkill['skill_type']
            card.activeSkill.levels = activeSkill['levels']
            card.activeSkill.maxTurns = activeSkill['turn_max']
            card.activeSkill.minTurns = activeSkill['turn_min']

            card.save()


        cards = CardNA.objects.all()
        for card in cards:
            print(card.activeSkill.name)





from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import CardNA, ActiveSkill
import requests
import json


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):
        cards = CardNA.objects.all()

        for card in cards:
            if card.activeSkill is None:
                print("No data")
            else:
                print(card.monster.name)
                print('\t\t', card.leaderSkill.name)
                print('\t\t', card.activeSkill.name)
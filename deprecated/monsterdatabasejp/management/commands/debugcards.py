from django.core.management.base import BaseCommand, CommandError
from monsters.models import CardNA, ActiveSkill, MonsterData
import requests
import json


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):
        cards = MonsterData.objects.all()

        for card in cards:
            print(card.awakenings.all())
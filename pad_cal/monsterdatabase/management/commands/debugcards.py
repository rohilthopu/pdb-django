from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import CardNA, ActiveSkill
import requests
import json


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):
        cards = CardNA.objects.all()

        for card in cards:
            print("Data Validity Check (Card Monster Data Name Type) :", type(card.monster.name))

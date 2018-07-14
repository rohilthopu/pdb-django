from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import CardNA, ActiveSkill, MonsterData
import requests
import json


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):
        tyrra = MonsterData.objects.get(name="Firedragon Tyrannos")

        print(tyrra.cardID)
        print(tyrra.ancestorID)
        for evo in tyrra.evolutions.all():
            print(evo)
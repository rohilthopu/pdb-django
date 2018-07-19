from django.core.management.base import BaseCommand
import requests
import json
from .dungeon_types import DUNGEON_TYPE, DUNGEON_TYPE_DESCRIPTORS, get_dungeon_type


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):

        link = "https://storage.googleapis.com/mirubot/paddata/processed/na_dungeons.json"

        data = requests.get(link).text
        pull = json.loads(data)

        for dungeon in pull:
            print(dungeon['unknown_004'])


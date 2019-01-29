from django.core.management.base import BaseCommand
import requests
import json
from dungeon.models import Dungeon, Floor
import time
import os
from .dungeon_parser.dungeon_parser import get_dungeon_list


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):
        def make_dungeon(item):
            dungeon = Dungeon()
            dungeon.name = item['clean_name'].rsplit("#")[-1]
            dungeon.dungeonID = item['dungeon_id']
            dungeon.floorCount = len(item['floors'])
            dungeon.dungeonType = item['alt_dungeon_type']
            dungeon.save()

        def make_dungeon_from_object(dungeon):
            item = Dungeon()
            dungeon.name = dungeon.clean_name
            dungeon.dungeonID = dungeon.dungeon_id
            dungeon.floorCount = len(dungeon.floors)
            dungeon.dungeonType = dungeon.alt_dungeon_type
            item.save()

        self.stdout.write(self.style.SUCCESS('Starting NA DUNGEON DB update.'))

        start = time.time()

        Dungeon.objects.all().delete()

        dungeon_list = get_dungeon_list()

        for item in dungeon_list:

            make_dungeon_from_object(item)

        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)

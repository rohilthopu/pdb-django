from django.core.management.base import BaseCommand
import json
from dungeon.models import EncounterSet
import time
import os
from .dungeon_wave_parser import parse_spawn_data
from dataversions.models import Version
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Starting Dungeon encounter build.'))

        start = time.time()

        prevSize = EncounterSet.objects.all().count()
        EncounterSet.objects.all().delete()

        print("Parsing values from csv")
        # call my wave parser to write to file
        parse_spawn_data.parse_waves()

        print("CSV -> JSON conversion complete")

        print("Importing new JSON data")

        if settings.DEBUG:
            location = '/Users/rohil/projects/personal/data_files/processed/wave_data.json'
        else:
            location = '/home/rohil/data/pad_data/processed_data/wave_data.json'

        with open(os.path.abspath(location), 'r') as jsonData:
            wave_data = json.load(jsonData)

        print("Parsing items")

        for item in wave_data:

            for floor in item['floors']:

                for wave in floor['waves']:
                    encounter_set = EncounterSet()

                    encounter_set.dungeon_id = item['dungeon_id']
                    encounter_set.floor_id = floor['floor']
                    encounter_set.wave_number = wave['wave']
                    encounter_set.encounter_data = json.dumps(wave['encounter_list'])
                    encounter_set.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('Encounter update complete.'))
        print("Elapsed time :", end - start)

        print("Updating version")

        ver = Version.objects.all()

        if len(ver) == 0:
            v = Version()
            v.monster = 1
            v.save()
        else:
            v = ver.first()
            if prevSize < EncounterSet.objects.all().count():
                v.monster += 1
            v.save()

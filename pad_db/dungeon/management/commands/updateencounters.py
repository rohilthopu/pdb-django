from django.core.management.base import BaseCommand
import json
from dungeon.models import EncounterSet
import time
import os
from .dungeon_wave_parser import parse_spawn_data
from dataversions.models import Version
from django.conf import settings
from Utils.progress import progress


class Command(BaseCommand):
    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Starting Dungeon encounter build.'))

        start = time.time()

        prevSize = EncounterSet.objects.all().count()
        EncounterSet.objects.all().delete()

        self.stdout.write("Parsing values from csv")
        # call my wave parser to write to file
        parse_spawn_data.parse_waves()

        self.stdout.write("CSV -> JSON conversion complete")

        self.stdout.write("Importing new JSON data")

        if settings.DEBUG:
            location = '/Users/rohil/projects/personal/data_files/processed/wave_data.json'
        else:
            location = '/home/rohil/data/pad_data/processed_data/wave_data.json'

        self.stdout.write('\tFile Location: {}'.format(location))

        with open(os.path.abspath(location), 'r') as jsonData:
            wave_data = json.load(jsonData)

        self.stdout.write("Parsing items")

        total = len(wave_data)

        for i in range(0, total):
            item = wave_data[i]

            progress(i, total)

            for floor in item['floors']:

                for wave in floor['waves']:
                    encounter_set = EncounterSet()
                    encounter_set.dungeon_id = item['dungeon_id']
                    encounter_set.floor_id = floor['floor']
                    encounter_set.wave_number = wave['wave']
                    encounter_set.encounter_data = json.dumps(wave['encounter_list'])
                    encounter_set.save()

        self.stdout.write('')
        end = time.time()
        self.stdout.write("Elapsed time : {}".format(end - start))
        self.stdout.write("Updating version")

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
        self.stdout.write(self.style.SUCCESS('Encounter update complete.'))

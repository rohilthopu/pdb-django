import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from guerrilla.models import GuerrillaDungeon
from pad_db.settings import DEBUG

DEVELOPMENT_PATH = '/Users/rohil/projects/personal/pdb_processor/output'
PRODUCTION_PATH = '/home/rohil/pdb-processor/output'
FILE_NAME = 'guerrilla_data.json'


@transaction.atomic
class Command(BaseCommand):
    help = "Updates the Guerrilla Dungeon List."

    def handle(self, *args, **options):

        if DEBUG:
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, FILE_NAME)), 'r') as guerrilla_data:
                guerrilla_dungeons = json.load(guerrilla_data)

        else:
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, FILE_NAME)), 'r') as guerrilla_data:
                guerrilla_dungeons = json.load(guerrilla_data)

        GuerrillaDungeon.objects.all().delete()

        for item in guerrilla_dungeons:
            dungeon = GuerrillaDungeon()
            dungeon.name = item['name']
            dungeon.start_time = item['start_time']
            dungeon.end_time = item['end_time']
            dungeon.startSecs = item['start_secs']
            dungeon.endSecs = item['end_secs']
            dungeon.group = item['group']
            dungeon.server = item['server']
            dungeon.dungeon_id = item['dungeon_id']
            dungeon.image_id = item['image_id']
            dungeon.save()

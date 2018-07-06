from django.core.management.base import BaseCommand, CommandError
from dungeon.models import Dungeon

class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):
        daily = Dungeon.objects.all()
        for item in daily:
            item.delete()
        self.stdout.write(self.style.SUCCESS('All dungeons successfully cleared!'))
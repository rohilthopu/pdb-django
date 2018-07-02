from django.core.management.base import BaseCommand, CommandError
from dungeon.models import DungeonToday

class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):
        daily = DungeonToday.objects.all()
        for item in daily:
            item.delete()
        self.stdout.write(self.style.SUCCESS('Daily dungeons successfully cleared!'))
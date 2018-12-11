from django.core.management.base import BaseCommand
from monsterdatabase.models import Monster, Evolution, Skill

class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        Monster.objects.all().delete()
        Evolution.objects.all().delete()
        Skill.objects.all().delete()
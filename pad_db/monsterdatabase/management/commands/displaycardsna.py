from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import Monster, Skill



class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):
        cards = Monster.objects.all()
        skills = Skill.objects.all()

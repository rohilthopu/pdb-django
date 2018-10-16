from django.db import models
from .choices import ISSUE_CHOICES, SERVER_CHOICES


# Create your models here.
class Issue(models.Model):
    server = models.CharField(default="", max_length=5, choices=SERVER_CHOICES)
    itemID = models.IntegerField(default=0)
    itemName = models.CharField(default="", max_length=100)
    itemType = models.CharField(default="", max_length=50, choices=sorted(ISSUE_CHOICES))
    description = models.TextField(default="")
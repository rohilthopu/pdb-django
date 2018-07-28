from django.db import models

class Bonus(models.Model):
    name = models.CharField(default="", max_length=100)

from django.db import models


# Create your models here.

class RedditUser(models.Model):
    author = models.CharField(max_length=50, default="")
    score = models.IntegerField(default=0)
    scoreUp = models.BooleanField(default=False)
    scoreDown = models.BooleanField(default=False)
    scoreDiff = models.IntegerField(default=0)
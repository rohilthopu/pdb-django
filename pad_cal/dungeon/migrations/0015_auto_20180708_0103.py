# Generated by Django 2.0.7 on 2018-07-08 06:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon', '0014_auto_20180706_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='dungeonID',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dungeontoday',
            name='listingDate',
            field=models.DateField(default=datetime.date(2018, 7, 8)),
        ),
    ]

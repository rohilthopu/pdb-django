# Generated by Django 2.0.7 on 2018-07-13 07:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dungeontoday',
            name='listingDate',
            field=models.DateField(default=datetime.date(2018, 7, 13)),
        ),
    ]

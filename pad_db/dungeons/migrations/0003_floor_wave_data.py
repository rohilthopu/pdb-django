# Generated by Django 2.0.7 on 2019-06-25 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeons', '0002_delete_encounterset'),
    ]

    operations = [
        migrations.AddField(
            model_name='floor',
            name='wave_data',
            field=models.TextField(default=''),
        ),
    ]

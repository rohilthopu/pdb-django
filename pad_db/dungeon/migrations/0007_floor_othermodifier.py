# Generated by Django 2.0.7 on 2018-12-18 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon', '0006_auto_20181217_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='floor',
            name='otherModifier',
            field=models.TextField(default=''),
        ),
    ]
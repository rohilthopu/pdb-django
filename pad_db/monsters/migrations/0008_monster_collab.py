# Generated by Django 2.0.7 on 2019-09-03 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0007_remove_monster_awakenings_raw'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='collab',
            field=models.CharField(default='', max_length=50),
        ),
    ]
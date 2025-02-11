# Generated by Django 2.0.7 on 2019-06-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GuerrillaDungeon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('start_time', models.CharField(default='', max_length=200)),
                ('end_time', models.CharField(default=0, max_length=200)),
                ('start_secs', models.FloatField(default=0)),
                ('end_secs', models.FloatField(default=0)),
                ('server', models.CharField(default='', max_length=10)),
                ('group', models.CharField(default='', max_length=5)),
                ('dungeon_id', models.IntegerField(default=-1)),
                ('image_id', models.IntegerField(default=1)),
            ],
        ),
    ]

# Generated by Django 2.0.7 on 2019-06-24 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_auto_20190623_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='atk_mult_full',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='skill',
            name='hp_mult_full',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='skill',
            name='rcv_mult_full',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='skill',
            name='shield_full',
            field=models.CharField(default='', max_length=20),
        ),
    ]
# Generated by Django 2.0.7 on 2018-12-06 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsterdatabasejp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monster',
            name='inheritable',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='monster',
            name='isCollab',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='monster',
            name='isReleased',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='monster',
            name='isUlt',
            field=models.CharField(default='', max_length=5),
        ),
    ]
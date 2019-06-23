# Generated by Django 2.0.7 on 2019-06-23 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0002_auto_20190622_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monster',
            name='inheritable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='monster',
            name='is_collab',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='monster',
            name='is_released',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='monster',
            name='is_ult',
            field=models.BooleanField(default=False),
        ),
    ]
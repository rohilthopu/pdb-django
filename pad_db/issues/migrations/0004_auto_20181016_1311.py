# Generated by Django 2.0.7 on 2018-10-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0003_issue_resolvestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='itemType',
            field=models.CharField(choices=[('', 'Select a problem child'), ('askill', 'Active Skill'), ('g', 'guerrilla'), ('lskill', 'LeaderSkill'), ('monster', 'Monster')], default='', max_length=50),
        ),
    ]

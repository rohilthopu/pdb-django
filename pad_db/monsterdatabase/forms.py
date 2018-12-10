from django import forms
from .models import Monster, Skill


class MonsterForm(forms.ModelForm):
    class Meta:
        model = Monster
        fields = (
            'name', 'cardID', 'rarity', 'cost', 'maxXP', 'inheritable', 'isCollab', 'isUlt', 'isReleased', 'maxLevel',
            'awakenings', 'superAwakenings', 'minHP', 'maxHP', 'hp99', 'minATK', 'maxATK', 'atk99', 'minRCV', 'maxRCV',
            'rcv99')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'cardID': forms.TextInput(attrs={'class': 'input'}),
            'rarity': forms.TextInput(attrs={'class': 'input'}),
            'cost': forms.TextInput(attrs={'class': 'input'}),
            'maxXP': forms.TextInput(attrs={'class': 'input'}),
            'inheritable': forms.TextInput(attrs={'class': 'input'}),
            'isCollab': forms.TextInput(attrs={'class': 'input'}),
            'isUlt': forms.TextInput(attrs={'class': 'input'}),
            'isReleased': forms.TextInput(attrs={'class': 'input'}),
            'maxLevel': forms.TextInput(attrs={'class': 'input'}),
            'awakenings': forms.Textarea(attrs={'class': 'textarea', }),
            'superAwakenings': forms.Textarea(attrs={'class': 'textarea'}),
            'minHP': forms.TextInput(attrs={'class': 'input'}),
            'maxHP': forms.TextInput(attrs={'class': 'input'}),
            'hp99': forms.TextInput(attrs={'class': 'input'}),
            'minATK': forms.TextInput(attrs={'class': 'input'}),
            'maxATK': forms.TextInput(attrs={'class': 'input'}),
            'atk99': forms.TextInput(attrs={'class': 'input'}),
            'minRCV': forms.TextInput(attrs={'class': 'input'}),
            'maxRCV': forms.TextInput(attrs={'class': 'input'}),
            'rcv99': forms.TextInput(attrs={'class': 'input'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = (
            'name', 'description', 'skillID', 'skill_type', 'hp_mult', 'atk_mult', 'rcv_mult',
            'dmg_reduction', 'c_skill_1', 'c_skill_2', 'c_skill_3', 'skill_class', 'levels', 'maxTurns',
            'minTurns'

        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.TextInput(attrs={'class': 'input'}),
            'skillID': forms.TextInput(attrs={'class': 'input'}),
            'skill_type': forms.TextInput(attrs={'class': 'input'}),
            'hp_mult': forms.TextInput(attrs={'class': 'input'}),
            'atk_mult': forms.TextInput(attrs={'class': 'input'}),
            'rcv_mult': forms.TextInput(attrs={'class': 'input'}),
            'dmg_reduction': forms.TextInput(attrs={'class': 'input'}),
            'c_skill_1': forms.TextInput(attrs={'class': 'input'}),
            'c_skill_2': forms.TextInput(attrs={'class': 'input'}),
            'c_skill_3': forms.TextInput(attrs={'class': 'input'}),
            'skill_class': forms.TextInput(attrs={'class': 'input'}),
            'levels': forms.TextInput(attrs={'class': 'input'}),
            'maxTurns': forms.TextInput(attrs={'class': 'input'}),
            'minTurns': forms.TextInput(attrs={'class': 'input'}),

        }


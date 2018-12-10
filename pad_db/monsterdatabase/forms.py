from django import forms
from .models import Monster


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
            'awakenings': forms.Textarea(attrs={'class': 'textarea',}),
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

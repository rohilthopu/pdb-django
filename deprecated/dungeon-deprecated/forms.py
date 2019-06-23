from django import forms

from .fields import MyModelChoiceField
from .models import Dungeon


class DungeonLink(forms.Form):
    dungeonLink = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ex. http://www.puzzledragonx.com/en/mission.asp?m=3021'}))



class DailyDungeonSelector(forms.Form):
    dungeon = MyModelChoiceField(queryset=Dungeon.objects.order_by('altTitle').all(), to_field_name="jpnTitle",
                                 empty_label='Choose a dungeons', )
    widgets = {
        'dungeons': forms.Select(attrs={'class': 'select'}),
    }

from django import forms

from .fields import MyModelChoiceField
from .models import Dungeon


class DungeonLink(forms.Form):
    dungeonLink = forms.CharField(max_length=50)


class DailyDungeonSelector(forms.Form):
    dungeon = MyModelChoiceField(queryset=Dungeon.objects.order_by('altTitle').all(), to_field_name="jpnTitle",
                                 empty_label='Choose a dungeon', )
    widgets = {
        'dungeon': forms.Select(
            attrs={'class': 'input-field'}),
    }
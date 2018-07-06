from django import forms
from .models import Dungeon, DungeonToday
from .fields import MyModelChoiceField

class DungeonLink(forms.Form):
    dungeonLink = forms.CharField(max_length=50)


class DailyDungeonSelector(forms.Form):
    dungeon = MyModelChoiceField(queryset=Dungeon.objects.all(), to_field_name="jpnTitle",
                                 empty_label='Choose a dungeon', )
    widgets = {
        'dungeon': forms.Select(
            attrs={'class': 'input-field'}),
    }
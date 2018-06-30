from django import forms

DAY_CHOICES = (
    ('', 'Select the Day'),
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

DAILY_CHOICES = (
    ('', 'Is this a daily dungeon?'),
    ('y', 'Yes'),
    ('n', 'No')

)

class DungeonLink(forms.Form):
    dungeonLink = forms.CharField(max_length=50)
    daily = forms.ChoiceField(choices=DAILY_CHOICES, required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES, required=False)


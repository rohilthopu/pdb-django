from django import forms

class DungeonLink(forms.Form):
    dungeonLink = forms.CharField(max_length=50)


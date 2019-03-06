from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        widgets = {
            'server': forms.Select(),
            'itemType': forms.Select(),
            'itemName': forms.TextInput(attrs={'class': 'input'}),
            'itemID': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea'})
        }

from django import forms
from .models import Suggestion

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'content', 'priority']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

class SuggestionUpdateForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['content', 'priority']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5, 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
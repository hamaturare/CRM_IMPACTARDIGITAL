from django import forms
from .models import Suggestion

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5})
        }

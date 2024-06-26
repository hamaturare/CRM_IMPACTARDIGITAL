from django import forms
from .models import Suggestion

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'content', 'priority', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SuggestionForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields.pop('status')

class SuggestionUpdateForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title','content', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5, 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

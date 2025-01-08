from django import forms
from .models import Movie

class MovieSearchForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['movie_name', 'year', 'genres']
        widgets = {
            'movie_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Name'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

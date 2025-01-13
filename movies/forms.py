# forms.py
from django import forms
from .models import Movie, MovieGenre, MovieStar, MovieDirector

class MovieSearchForm(forms.Form):
    name = forms.CharField(required=False, label="Movie Name")
    year = forms.IntegerField(required=False, label="Release Year")
    genre = forms.ModelChoiceField(
        queryset=MovieGenre.objects.all(),
        required=False,
        label="Genre"
    )
    actor = forms.ModelChoiceField(
        queryset=MovieStar.objects.all(),
        required=False,
        label="Actor"
    )
    director = forms.ModelChoiceField(
        queryset=MovieDirector.objects.all(),
        required=False,
        label="Director"
    )


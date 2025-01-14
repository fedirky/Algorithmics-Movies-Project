# forms.py
from django import forms
from .models import Movie, MovieGenre, MovieStar, MovieDirector

AGE_CERTIFICATES = [
    ('G', 'G - General Audiences'),
    ('PG', 'PG - Parental Guidance Suggested'),
    ('PG-13', 'PG-13 - Parents Strongly Cautioned'),
    ('R', 'R - Restricted'),
    ('NC-17', 'NC-17 - Adults Only'),
]

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
    certificates = forms.MultipleChoiceField(
        choices=AGE_CERTIFICATES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Age Rating"
    )

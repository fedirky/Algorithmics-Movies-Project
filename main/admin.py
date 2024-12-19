from django.contrib import admin
from .models import MovieGenre, MovieDirector, MovieStar, Movie

admin.site.register(MovieGenre)

admin.site.register(MovieDirector)

admin.site.register(MovieStar)

admin.site.register(Movie)

#from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Movie

class TopRatedMoviesView(ListView):
    model = Movie
    template_name = 'movies/top_rated.html'
    context_object_name = 'movies'
    paginate_by = 20

    def get_queryset(self):
        return Movie.objects.all().order_by('-rating')[:20]
    
class MoviePage(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_object(self):
        # Отримуємо фільм за `movie_id`, який передається в URL
        movie_id = self.kwargs.get('movie_id')
        return get_object_or_404(Movie, movie_id=movie_id)


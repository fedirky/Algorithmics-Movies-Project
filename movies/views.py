#from django.shortcuts import render

from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Movie
from .forms import MovieSearchForm


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


class MovieSearchView(ListView):
    model = Movie
    template_name = 'movies/search_movies.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.get_form()
        if form.is_valid():
            name = form.cleaned_data.get('name')
            year = form.cleaned_data.get('year')
            genre = form.cleaned_data.get('genre')

            if name:
                queryset = queryset.filter(movie_name__icontains=name)
            if year:
                queryset = queryset.filter(year=year)
            if genre:
                queryset = queryset.filter(genres=genre)
        return queryset

    def get_form(self):
        return MovieSearchForm(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


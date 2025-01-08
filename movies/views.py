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

class MovieSearchView(FormView):
    template_name = 'movies/search_form.html'
    form_class = MovieSearchForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        query_results = None

        if form.is_valid():
            query_results = self.get_queryset(form)
        
        return self.render_to_response(self.get_context_data(form=form, results=query_results))

    def get_queryset(self, form):
        # Отримуємо дані з форми
        movie_name = form.cleaned_data.get('movie_name')
        year = form.cleaned_data.get('year')
        genres = form.cleaned_data.get('genres')

        # Створюємо базовий запит
        query_results = Movie.objects.all()

        if movie_name:
            query_results = query_results.filter(movie_name__icontains=movie_name)
        if year:
            query_results = query_results.filter(year=year)
        if genres.exists():
            query_results = query_results.filter(genres__in=genres).distinct()

        return query_results

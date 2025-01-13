#from django.shortcuts import render

from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Movie
from .forms import MovieSearchForm

from django.views import View
from django.contrib import messages
from users.models import MovieWatch, UserProfile
from django.utils.timezone import now


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
            actor = form.cleaned_data.get('actor')
            director = form.cleaned_data.get('director')
            sort = self.request.GET.get('sort')  # Отримуємо параметр сортування

            if name:
                queryset = queryset.filter(movie_name__icontains=name)
            if year:
                queryset = queryset.filter(year=year)
            if genre:
                queryset = queryset.filter(genres__name__icontains=genre)
            if actor:
                queryset = queryset.filter(stars__name__icontains=actor)
            if director:
                queryset = queryset.filter(directors__name__icontains=director)
            
            # Застосовуємо сортування за рейтингом
            if sort == 'asc':
                queryset = queryset.order_by('rating')
            elif sort == 'desc':
                queryset = queryset.order_by('-rating')

        return queryset.distinct()

    def get_form(self):
        return MovieSearchForm(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class MovieWatchUpdateView(View):
    template_name = 'movies/movie_watch_form.html'

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        profile = get_object_or_404(UserProfile, user=request.user)

        # Отримання або створення MovieWatch
        movie_watch, created = MovieWatch.objects.get_or_create(
            movie=movie,
            user_profile=profile,
            defaults={'watched_at': now(), 'is_finished': False, 'rating': 0}
        )

        return render(request, self.template_name, {
            'movie': movie,
            'movie_watch': movie_watch,
        })

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        profile = get_object_or_404(UserProfile, user=request.user)
        movie_watch = get_object_or_404(MovieWatch, movie=movie, user_profile=profile)

        # Оновлення даних MovieWatch
        movie_watch.is_finished = 'is_finished' in request.POST
        movie_watch.rating = int(request.POST.get('rating', 0))
        movie_watch.watched_at = request.POST.get('watched_at', movie_watch.watched_at)
        movie_watch.save()

        messages.success(request, 'Watch details updated successfully!')
        return redirect('movie_detail', movie_id=movie.movie_id)

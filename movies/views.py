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

from collections import Counter
from itertools import combinations

import json


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
        movie = get_object_or_404(Movie, id=movie_id)  # Використання movie_id
        profile = get_object_or_404(UserProfile, user=request.user)
        movie_watch = get_object_or_404(MovieWatch, movie=movie, user_profile=profile)

        # Оновлення даних MovieWatch
        movie_watch.is_finished = 'is_finished' in request.POST
        movie_watch.rating = int(request.POST.get('rating', 0))
        movie_watch.watched_at = request.POST.get('watched_at', movie_watch.watched_at)
        movie_watch.save()

        # Отримання нових рекомендацій
        recommendations_dictionary = recommended_movies(profile)

        # Оновлення рекомендацій у профілі користувача
        profile.priority_movies_recommendations_dictionary = json.dumps(recommendations_dictionary)
        profile.save()

        messages.success(request, 'Watch details and recommendations updated successfully!')
        return redirect('movie_detail', movie_id=movie.movie_id)
    

def recommended_movies(user_profile):
    """
    Функція для отримання списку фільмів з високою і низькою пріоритетністю на основі спільних тегів.
    Відкидаються фільми, рейтинг яких менший за 6.
    """
    liked_movies = MovieWatch.objects.filter(
        user_profile=user_profile, rating=1
    ).select_related('movie').prefetch_related(
        'movie__genres', 'movie__directors', 'movie__stars'
    ).order_by('-watched_at')[:10]

    genres = Counter()
    directors = Counter()
    stars = Counter()

    for watch in liked_movies:
        movie = watch.movie
        genres.update(genre.name for genre in movie.genres.all())
        directors.update(director.name for director in movie.directors.all())
        stars.update(star.name for star in movie.stars.all())

    # Формуємо список тегів, що з'являються більше двох разів
    tags = (
        [f'genre:{genre}' for genre, count in genres.items() if count >= 2] +
        [f'director:{director}' for director, count in directors.items() if count >= 2] +
        [f'star:{star}' for star, count in stars.items() if count >= 2]
    )
    watched_movies_ids = set(
        MovieWatch.objects.filter(user_profile=user_profile).values_list('movie__movie_id', flat=True)
    )
    high_priority_movies = set()
    low_priority_movies = set()

    # Перебираємо всі комбінації від максимальної до мінімальної кількості тегів
    for r in range(len(tags), 0, -1):
        for tag_combo in combinations(tags, r):
            movies = Movie.objects.filter(rating__gte=6)  # Відкидаємо фільми з рейтингом < 6
            for tag in tag_combo:
                key, value = tag.split(':')
                if key == 'genre':
                    movies = movies.filter(genres__name=value)
                elif key == 'director':
                    movies = movies.filter(directors__name=value)
                elif key == 'star':
                    movies = movies.filter(stars__name=value)
            movies = movies.distinct()

            # Класифікуємо фільми за пріоритетністю
            if r >= 3:
                high_priority_movies.update(movie.movie_id for movie in movies)
            elif r <= 2:
                low_priority_movies.update(movie.movie_id for movie in movies)

    return {
        'high_priority_movies': list(high_priority_movies - watched_movies_ids),
        'low_priority_movies': list(set(low_priority_movies - high_priority_movies - watched_movies_ids)),
    }


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Movie, MovieWatch
from collections import Counter


def index_page(request):
    return render(request, 'index.html')


@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    movie_watches = user_profile.movie_watches.all()
    
    return render(request, 'users/profile.html', {'profile': user_profile, 'movie_watches': movie_watches})


from itertools import combinations
from django.db.models import Q
from collections import Counter

@login_required
def common_movie_features(request):
    """
    Відображає фільми, які мають найбільше спільних рис із переглянутими фільмами користувача.
    Спочатку шукаються всі комбінації з максимальним числом тегів, потім поступово зменшується кількість тегів.
    """
    user_profile = request.user.userprofile
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

    # Debug: Вивід кількості тегів і їх список
    print(f"Number of tags found: {len(tags)}")
    print(f"Tags: {tags}")

    found_movies = []

    # Перебираємо всі комбінації від максимальної до мінімальної кількості тегів
    for r in range(len(tags), 0, -1):
        for tag_combo in combinations(tags, r):
            print(f"Processing combination: {tag_combo}")  # Debug
            movies = Movie.objects.all()
            for tag in tag_combo:
                key, value = tag.split(':')
                if key == 'genre':
                    movies = movies.filter(genres__name=value)
                elif key == 'director':
                    movies = movies.filter(directors__name=value)
                elif key == 'star':
                    movies = movies.filter(stars__name=value)
            movies = movies.distinct().order_by('-rating')[:5]
            if movies.exists():
                found_movies.append((tag_combo, movies))

    return render(request, 'users/recommendations.html', {
        'user_profile': user_profile,
        'found_movies': found_movies,
        'tags': tags,
    })


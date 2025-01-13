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


@login_required
def common_movie_features(request):
    """
    Відображає спільні риси фільмів, які отримали рейтинг 'Liked' від поточного користувача,
    а також список до 5 найкращих фільмів для кожної з цих рис.
    Аналізується лише останні 10 фільмів, переглянутих користувачем.
    """
    user_profile = request.user.userprofile  # Отримуємо профіль поточного користувача
    liked_movies = MovieWatch.objects.filter(user_profile=user_profile, rating=1).select_related('movie').prefetch_related('movie__genres', 'movie__directors', 'movie__stars').order_by('-watched_at')[:10]

    genres = Counter()
    directors = Counter()
    stars = Counter()

    # Рахуємо частоту кожної риси для останніх 10 фільмів
    for watch in liked_movies:
        movie = watch.movie
        genres.update(genre.name for genre in movie.genres.all())
        directors.update(director.name for director in movie.directors.all())
        stars.update(star.name for star in movie.stars.all())

    # Фільтруємо риси, які з'являються хоча б двічі
    common_features = {
        "genres": [f"{genre} ({count})" for genre, count in genres.items() if count >= 2],
        "directors": [f"{director} ({count})" for director, count in directors.items() if count >= 2],
        "stars": [f"{star} ({count})" for star, count in stars.items() if count >= 2],
    }

    # Знаходимо до 5 найкращих фільмів для кожної риси
    top_movies_by_feature = {
        "genres": {},
        "directors": {},
        "stars": {},
    }

    for genre in common_features['genres']:
        genre_name = genre.split(' (')[0]  # Видаляємо лічильник для запиту
        top_movies_by_feature['genres'][genre] = Movie.objects.filter(genres__name=genre_name).order_by('-rating')[:5]

    for director in common_features['directors']:
        director_name = director.split(' (')[0]  # Видаляємо лічильник для запиту
        top_movies_by_feature['directors'][director] = Movie.objects.filter(directors__name=director_name).order_by('-rating')[:5]

    for star in common_features['stars']:
        star_name = star.split(' (')[0]  # Видаляємо лічильник для запиту
        top_movies_by_feature['stars'][star] = Movie.objects.filter(stars__name=star_name).order_by('-rating')[:5]

    # Рахуємо кількість фільмів кожного тегу, режисера та актора
    tag_count = {
        "genres": genres,
        "directors": directors,
        "stars": stars,
    }

    return render(request, 'users/recommendations.html', {
        'user_profile': user_profile,
        'common_features': common_features,
        'top_movies_by_feature': top_movies_by_feature,
        'tag_count': tag_count,
    })


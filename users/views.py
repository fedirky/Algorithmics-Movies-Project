from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Movie, MovieWatch
from collections import Counter


@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    movie_watches = user_profile.movie_watches.all()
    
    return render(request, 'users/profile.html', {'profile': user_profile, 'movie_watches': movie_watches})


@login_required
def common_movie_features(request):
    """
    Відображає спільні риси фільмів, які отримали рейтинг 'Liked' від поточного користувача,
    а також список до 100 найкращих фільмів для кожної з цих рис.
    """
    user_profile = request.user.userprofile  # Отримуємо профіль поточного користувача
    liked_movies = MovieWatch.objects.filter(user_profile=user_profile, rating=1).select_related('movie').prefetch_related('movie__genres', 'movie__directors', 'movie__stars')
    
    genres = Counter()
    directors = Counter()
    stars = Counter()

    for watch in liked_movies:
        movie = watch.movie
        genres.update(genre.name for genre in movie.genres.all())
        directors.update(director.name for director in movie.directors.all())
        stars.update(star.name for star in movie.stars.all())

    # Фільтруємо спільні риси, які зустрічаються у всіх лайкнутих фільмах
    total_liked = liked_movies.count()
    common_features = {
        "genres": [genre for genre, count in genres.items() if count == total_liked],
        "directors": [director for director, count in directors.items() if count == total_liked],
        "stars": [star for star, count in stars.items() if count == total_liked],
    }

    # Знаходимо до 100 найкращих фільмів для кожної риси
    top_movies_by_feature = {
        "genres": {},
        "directors": {},
        "stars": {},
    }

    for genre in common_features['genres']:
        top_movies_by_feature['genres'][genre] = Movie.objects.filter(genres__name=genre).order_by('-rating')[:5]

    for director in common_features['directors']:
        top_movies_by_feature['directors'][director] = Movie.objects.filter(directors__name=director).order_by('-rating')[:5]

    for star in common_features['stars']:
        top_movies_by_feature['stars'][star] = Movie.objects.filter(stars__name=star).order_by('-rating')[:5]

    return render(request, 'users/recommendations.html', {
        'user_profile': user_profile,
        'common_features': common_features,
        'top_movies_by_feature': top_movies_by_feature,
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, MovieWatch
from collections import Counter


@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    movie_watches = user_profile.movie_watches.all()
    
    return render(request, 'users/profile.html', {'profile': user_profile, 'movie_watches': movie_watches})


@login_required
def common_movie_features(request):
    """
    Відображає спільні риси фільмів, які отримали рейтинг 'Liked' від поточного користувача.
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

    return render(request, 'users/recommendations.html', {
        'user_profile': user_profile,
        'common_features': common_features,
    })
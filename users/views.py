from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Movie, MovieWatch
from collections import Counter
from itertools import combinations
import json


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
    Відображає рекомендовані фільми з профілю користувача.
    Спочатку відображаються "Highly Recommended Films", потім "Films You Would Like".
    """
    user_profile = request.user.userprofile

    # Завантаження рекомендацій зі словника профілю
    recommendations = json.loads(user_profile.priority_movies_recommendations_dictionary or '{}')

    # Розділення на категорії
    highly_recommended = recommendations.get('high_priority_movies', [])
    films_you_would_like = recommendations.get('low_priority_movies', [])

    # Отримання випадкових 10 фільмів із кожної категорії
    highly_recommended_movies = Movie.objects.filter(movie_id__in=highly_recommended).order_by('?')[:10]
    films_you_would_like_movies = Movie.objects.filter(movie_id__in=films_you_would_like).order_by('?')[:10]

    return render(request, 'users/recommendations.html', {
        'user_profile': user_profile,
        'highly_recommended_movies': highly_recommended_movies,
        'films_you_would_like_movies': films_you_would_like_movies,
    })

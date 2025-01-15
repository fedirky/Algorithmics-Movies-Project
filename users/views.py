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
def recommended_movies_render(request):
    """
    Відображає рекомендовані фільми з профілю користувача.
    Відображаються категорії: "Highly Recommended Films", "Films You Would Like",
    "Popular Films", "Kids Films" та "Recent Films".
    """
    user_profile = request.user.userprofile

    # Завантаження рекомендацій зі словника профілю
    recommendations = json.loads(user_profile.priority_movies_recommendations_dictionary or '{}')

    # Розділення на категорії
    highly_recommended = recommendations.get('high_priority_movies', [])
    films_you_would_like = recommendations.get('low_priority_movies', [])
    popular_movies = recommendations.get('popular_movies', [])
    kids_movies = recommendations.get('kids_movies', [])
    recent_movies = recommendations.get('recent_movies', [])

    # Отримання випадкових 10 фільмів із кожної категорії
    highly_recommended_movies = Movie.objects.filter(movie_id__in=highly_recommended).order_by('?')[:5]
    films_you_would_like_movies = Movie.objects.filter(movie_id__in=films_you_would_like).order_by('?')[:5]
    popular_movies_list = Movie.objects.filter(movie_id__in=popular_movies).order_by('?')[:5]
    kids_movies_list = Movie.objects.filter(movie_id__in=kids_movies).order_by('?')[:5]
    recent_movies_list = Movie.objects.filter(movie_id__in=recent_movies).order_by('?')[:5]

    return render(request, 'users/recommendations.html', {
        'user_profile': user_profile,
        'highly_recommended_movies': highly_recommended_movies,
        'films_you_would_like_movies': films_you_would_like_movies,
        'popular_movies': popular_movies_list,
        'kids_movies': kids_movies_list,
        'recent_movies': recent_movies_list,
    })

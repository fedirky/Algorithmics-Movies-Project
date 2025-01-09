from django.urls import path
from .views import TopRatedMoviesView, MoviePage, MovieSearchView

urlpatterns = [
    path('top-rated/', TopRatedMoviesView.as_view(), name='top_rated_movies'),
    path('movie/<str:movie_id>/', MoviePage.as_view(), name='movie_detail'),
    path('search/', MovieSearchView.as_view(), name='movie_search'),
]


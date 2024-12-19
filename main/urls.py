from django.urls import path
from main.views import TopRatedMoviesView, MoviePage

urlpatterns = [
    path('top-rated/', TopRatedMoviesView.as_view(), name='top_rated_movies'),
    path('movie/<str:movie_id>/', MoviePage.as_view(), name='movie_detail'),
]


from django.urls import path
from .views import TopRatedMoviesView, MoviePage, MovieSearchView, MovieWatchUpdateView

urlpatterns = [
    path('top-rated/', TopRatedMoviesView.as_view(), name='top_rated_movies'),
    path('movie/<str:movie_id>/', MoviePage.as_view(), name='movie_detail'),
    path('search/', MovieSearchView.as_view(), name='movie_search'),
    path('movie/<int:movie_id>/watch/', MovieWatchUpdateView.as_view(), name='movie_watch_add_or_update'),

]


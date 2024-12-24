from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    liked_movies = models.ManyToManyField(Movie, related_name='liked_by_users')
    disliked_movies = models.ManyToManyField(Movie, related_name='disliked_by_users')

    def __str__(self):
        return self.user.username


class MovieWatch(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='movie_watches')
    is_finished = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f'{self.movie.movie_name} - Watched: {self.is_finished}'



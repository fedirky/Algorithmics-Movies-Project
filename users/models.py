from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class MovieWatch(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='movie_watches')
    watched_at = models.DateTimeField(auto_now_add=False)
    is_finished = models.BooleanField(default=False)
    rating = models.IntegerField(default=0, choices=[(-1, 'Disliked'), (0, 'Neutral'), (1, 'Liked')])

    def __str__(self):
        return f'{self.movie.movie_name} - Watched: {self.is_finished}, Rating: {self.get_rating_display()}'


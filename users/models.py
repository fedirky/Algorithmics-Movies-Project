from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    liked_movies = models.ManyToManyField(Movie, related_name='liked_by_users')
    disliked_movies = models.ManyToManyField(Movie, related_name='disliked_by_users')

    def __str__(self):
        return self.user.username

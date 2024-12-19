from django.db import models


class MovieGenre(models.Model):
    name =  models.TextField()
    def __str__(self):
        return self.name


class MovieDirector(models.Model):
    name =  models.TextField()
    def __str__(self):
        return self.name


class MovieStar(models.Model):
    name =  models.TextField()
    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.TextField()
    movie_name = models.TextField()
    description = models.TextField()

    year = models.IntegerField()
    certificate = models.TextField()
    runtime = models.IntegerField()

    genres = models.ManyToManyField(MovieGenre,  blank = True)
    rating = models.FloatField()
    
    directors  = models.ManyToManyField(MovieDirector,  blank = True)
    #directorID

    stars  = models.ManyToManyField(MovieStar,  blank = True)
    #starID

    votes   = models.IntegerField()
    #gross(in $)

    def __str__(self):
        return self.movie_name

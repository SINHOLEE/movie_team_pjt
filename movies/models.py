from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass

class Genre(models.Model):
    genreNm = models.CharField(max_length=200)
    def __str__(self):
        return self.genreNm

class Director(models.Model):
    directorNm = models.CharField(max_length=200)
    def __str__(self):
        return self.directorNm

class Actor(models.Model):
    actorNm = models.CharField(max_length=200)
    def __str__(self):
        return self.actorNm


class Movie(models.Model):
    movieNm = models.CharField(max_length=200)
    poster_url = models.CharField(max_length=500)
    link_url = models.CharField(max_length=500)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    comment = models.CharField(max_length=200)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)



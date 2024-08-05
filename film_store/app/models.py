from django.db import models
from django.contrib.auth.models import AbstractUser


class Genre(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    director = models.CharField(max_length=255)
    release_year = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    duration = models.IntegerField()
    video_url = models.TextField()
    cover_image_url = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class GeneralUser(AbstractUser):
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    email = models.EmailField(unique=True)
    films = models.ManyToManyField(Film)

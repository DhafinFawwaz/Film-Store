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

    # change the upload_to if we're going to use cloud storage
    video = models.FileField(upload_to='videos/', null=True) # In actual implementation, this wont be null. Just for Django to work
    cover_image = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GeneralUser(AbstractUser):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    email = models.EmailField(unique=True)
    bought_films = models.ManyToManyField(Film)
    wishlist_films = models.ManyToManyField(Film, related_name='wishlist')
    
class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(GeneralUser, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True) # 1-5
    review = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

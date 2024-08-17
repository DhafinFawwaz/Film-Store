from typing import Iterable
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

    video = models.FileField(upload_to='videos/', null=True)
    cover_image = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: denormalize
    # avg_rating = models.IntegerField()

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

    # TODO: denormalize
    # def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
    #     return super().save(force_insert, force_update, using, update_fields)
    #     # case insert
    #     avg_rating = (current_avg_rating * current_total_rating + new_rating) / (current_total_rating + 1)
    #     # case update
    #     avg_rating = (current_avg_rating * current_total_rating - old_rating + new_rating) / current_total_rating
    #     # case delete
    #     avg_rating = (current_avg_rating * current_total_rating - old_rating) / (current_total_rating - 1)
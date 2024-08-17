from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app.models import Review

@receiver(post_save, sender=Review)
def invalidate_review_cache(sender, instance: Review, **kwargs):
    print("\033[93minvalidating Cache after review save\033[0m")
    film_id = instance.film.id

    # Page
    cache_keys = f"reviews_film_{film_id}_page_*"
    print(f"cache_keys: {cache_keys}")
    cache.delete_many(cache.keys(cache_keys))

    # Film
    cache_keys = f"film_{film_id}"
    print(f"cache_keys: {cache_keys}")
    cache.delete_many(cache.keys(cache_keys))

@receiver(post_delete, sender=Review)
def invalidate_review_cache_on_delete(sender, instance: Review, **kwargs):
    print("\033[93minvalidating Cache after review delete\033[0m")
    film_id = instance.film.id

    # Page
    cache_keys = f"reviews_film_{film_id}_page_*"
    print(f"cache_keys: {cache_keys}")
    cache.delete_many(cache.keys(cache_keys))
    
    # Film
    cache_keys = f"film_{film_id}"
    print(f"cache_keys: {cache_keys}")
    cache.delete_many(cache.keys(cache_keys))

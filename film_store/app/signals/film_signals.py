from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app.models import Film

@receiver(post_save, sender=Film)
def invalidate_film_cache(sender, instance, **kwargs):
    print("\033[93minvalidating Cache after film save\033[0m")
    cache_keys = cache.keys("films_page_*")
    cache.delete_many(cache_keys)

@receiver(post_delete, sender=Film)
def invalidate_film_cache_on_delete(sender, instance, **kwargs):
    print("\033[93minvalidating Cache after film delete\033[0m")
    cache_keys = cache.keys("films_page_*")
    cache.delete_many(cache_keys)

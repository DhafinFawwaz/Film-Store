from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app.models import Review

@receiver(post_save, sender=Review)
def invalidate_review_cache(sender, instance, **kwargs):
    print("\033[93minvalidating Cache after review save\033[0m")
    cache_keys = cache.keys("reviews_page_*")
    cache.delete_many(cache_keys)

@receiver(post_delete, sender=Review)
def invalidate_review_cache_on_delete(sender, instance, **kwargs):
    print("\033[93minvalidating Cache after review delete\033[0m")
    cache_keys = cache.keys("reviews_page_*")
    cache.delete_many(cache_keys)

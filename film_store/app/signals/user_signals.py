from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from app.models import GeneralUser


# bought_films
@receiver(m2m_changed, sender=GeneralUser.bought_films.through)
def invalidate_user_cache_on_bought_film_change(sender, instance, **kwargs):
    print("\033[93minvalidating Cache after bough films change\033[0m")
    user_id = instance.id
    cache_keys = f"user_{user_id}_bought_films_page_*"
    print(f"cache_keys: {cache_keys}")
    cache.delete_many(cache.keys(cache_keys))

# wishlist_films
@receiver(m2m_changed, sender=GeneralUser.wishlist_films.through)
def invalidate_user_cache_on_wishlist_film_change(sender, instance, **kwargs):
    print("\033[93minvalidating Cache after wishlist films change\033[0m")
    user_id = instance.id
    cache_keys = f"user_{user_id}_wishlist_films_page_*"
    print(f"cache_keys: {cache_keys}")
    cache.delete_many(cache.keys(cache_keys))
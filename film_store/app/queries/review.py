from app.api.api_request import APIRequest
from app.models import Film, Review
from django.db.models import Q
from django.db.models.manager import BaseManager
from django.core.cache import cache
from app.utils import clamp
from django.core.paginator import Paginator
import json
from app.serializers import FilmViewContextSerializer, ReviewViewContextSerializer
from django.core.serializers.json import DjangoJSONEncoder
from app.views.views_decorator import timeit
from datetime import datetime
from typing import Callable


def find_reviews(film: Film):
    return Review.objects.filter(film=film).exclude(review__isnull=True).order_by('-updated_at')
    
@timeit("Get Paginated Reviews")
def find_and_populate_paginated_film_review(request: APIRequest, context: dict, film: Film):
    page = request.GET.get('page', 1)
    try: page = int(page)
    except: page = 1
    cache_key = f"reviews_film_{film.id}_page_{page}"
    cached_reviews = None
    print(f"cache_key: {cache_key}")
    try: cached_reviews = cache.get(cache_key)
    except Exception as e:
        print(f"\033[91mError: Getting cache failed. {e}\033[0m")
        cached_reviews = None

    reviews_ctx = None
    elided_page = None
    num_pages = None
    iat = None
    
    if cached_reviews:
        print("\033[92mCache hit\033[0m")
        data = json.loads(cached_reviews)

        reviews_ctx = data['reviews']
        elided_page = data['elided_page']
        num_pages = data['num_pages']
        iat = datetime.fromisoformat(data['iat'])
    else:
        print("\033[93mCache miss\033[0m")
        film = Film.objects.get(id=film.id) # get the updated film
        reviews = find_reviews(film)
        paginator = Paginator(reviews, 8)
        page = clamp(page, 1, paginator.num_pages)
        reviews = paginator.get_page(page)
        reviews_ctx = ReviewViewContextSerializer(reviews, many=True).data
        elided_page = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
        elided_page = [page for page in elided_page]
        num_pages = paginator.num_pages
        try: cache.set(cache_key, json.dumps({
                'reviews': reviews_ctx,
                'elided_page': elided_page,
                'num_pages': num_pages,
                'iat': datetime.now()
            }, cls=DjangoJSONEncoder))
        except Exception as e:
            print(f"\033[91mError: Setting cache failed. {e}\033[0m")

    context['elided_page'] = elided_page
    context['prev_page'] = page - 1 if page > 1 else None
    context['next_page'] = page + 1 if page < num_pages else None
    context['current_page'] = page
    context['all_review'] = reviews_ctx
    context['iat'] = iat if iat else datetime.now()
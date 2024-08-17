from app.api.api_request import APIRequest
from app.models import Film
from django.db.models import Q
from django.db.models.manager import BaseManager
from django.core.cache import cache
from app.utils import clamp
from django.core.paginator import Paginator
import json
from app.serializers import FilmViewContextSerializer
from django.core.serializers.json import DjangoJSONEncoder
from app.views.views_decorator import timeit
from datetime import datetime



def find_film(request: APIRequest) -> BaseManager[Film]:
    films = []
    if 'q' in request.GET and request.GET['q'] != '':
        query = request.GET['q']
        films = Film.objects.filter(
            Q(title__icontains=query) | Q(director__icontains=query)
        ).order_by('-release_year')
    else:
        films = Film.objects.all().order_by('-release_year')
    return films

@timeit("Get Paginated Films")
def find_and_populate_paginated_film(request: APIRequest, context: dict, query: str = None):
    page = int(request.GET.get('page', 1))

    cache_key = None
    cached_films = None
    try:
        cache_key = f"films_page_{page}_query_{query}" if query else f"films_page_{page}_all"
        cached_films = cache.get(cache_key)
    except Exception as e:
        print(f"\033[91mError: Getting cache failed. {e}\033[0m")
        cached_films = None

    films_ctx = None
    elided_page = None
    num_pages = None
    iat = None
    
    if cached_films:
        print("\033[92mCache hit\033[0m")
        data = json.loads(cached_films)

        films_ctx = data['films']
        elided_page = data['elided_page']
        num_pages = data['num_pages']
        iat = datetime.fromisoformat(data['iat'])
    else:
        print("\033[93mCache miss\033[0m")
        films = find_film(request)
        paginator = Paginator(films, 8)
        page = clamp(page, 1, paginator.num_pages)
        films = paginator.get_page(page)
        films_ctx = FilmViewContextSerializer(films, many=True).data
        elided_page = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
        elided_page = [page for page in elided_page]
        num_pages = paginator.num_pages
        try:
            cache.set(cache_key, json.dumps({
                'films': films_ctx,
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
    context['films'] = films_ctx
    context['iat'] = iat if iat else datetime.now()
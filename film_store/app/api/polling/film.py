from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from app.api.api_response import APIResponse
from app.models import GeneralUser
from app.serializers import GeneralUserSerializer
from django.db.utils import IntegrityError
from rest_framework.serializers import ValidationError
from app.api.route_decorator import protected, public
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from app.api.api_request import APIRequest
from app.auth.token import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, authentication_classes
from django.shortcuts import redirect
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from app.api.swagger.auth_schemas import LoginFormBody, RegisterFormBody, LoginResponse, RegisterResponse, LogoutResponseSchema, SelfResponse, UsersResponse
from app.api.swagger.film_schemas import FilmResponse, FilmDetailResponse
from app.api.swagger.api_response_schema import APIErrorResponse
from time import sleep
from django.core.cache import cache
from datetime import datetime
from app.queries.film import find_and_populate_paginated_all_film, find_and_populate_paginated_bought_film, find_and_populate_paginated_wishlist_film, populate_film_details
from app.queries.review import find_and_populate_paginated_film_review
import json
from typing import Callable
from app.models import Film
from drf_yasg import openapi
from uuid import uuid4



def process_polling(request: APIRequest, cache_key: str, find_film_func: Callable):
    user_id = request.user.id
    user_poll_key = f"user_{user_id}_poll_uuid"
    initial_user_poll_uuid = uuid4()
    cache.set(user_poll_key, initial_user_poll_uuid)


    print(f"User {user_id} polling {cache_key} with poll uuid {initial_user_poll_uuid}")
    try:
        data = cache.get(cache_key)
        if not data:
            return APIResponse(data=None, status=status.HTTP_204_NO_CONTENT)
        data = json.loads(data)
        iat = datetime.fromisoformat(data['iat'])

        might_be_new_data = None

        max_wait = 30
        waited = 0
        sleep_time = 2

        data = {}
        while True:
            current_user_poll_uuid = cache.get(user_poll_key)
            if current_user_poll_uuid != initial_user_poll_uuid: # cancel request if same user polling more than 1
                # print(f"User {current_user_poll_uuid} polling more than 1. Cancel request.")
                return APIResponse(data=None, status=status.HTTP_204_NO_CONTENT)
            

            # print(f"{waited} s | Waiting for new data.")
            might_be_new_data = cache.get(cache_key)
            if not might_be_new_data: # case cache invalidated when saving models
                print("\033[94mCache invalidated. Re-fetching data.\033[0m")
                req = request
                find_film_func(req, data)
                break

            else: # case another request updated the cache. Should be very rare because the cache should already be invalidated
                might_be_new_data = json.loads(might_be_new_data)
                might_be_new_datetime = datetime.fromisoformat(might_be_new_data['iat'])
                if might_be_new_datetime != iat: # if this equals, then cache is still the same. Not modified by other request
                    find_film_func(req, data)
                    print("\033[94mNew data available.\033[0m")
                    break 
        
            sleep(sleep_time)
            waited += sleep_time
            if waited >= max_wait: 
                return APIResponse(data=None, status=status.HTTP_204_NO_CONTENT)
        
        return APIResponse(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return APIResponse(data=None, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    operation_summary="Polling search film",
    operation_description="Find film by search query or page. Will response when new data is available.",
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Search for films by title and director"),
        openapi.Parameter('Page', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Get films in certain page")
    ],
    responses={
        200: FilmResponse,
        204: FilmResponse,
    },
    method="GET"
)
@api_view(['GET'])
@protected
def film_polling(request: APIRequest, *args, **kwargs):
    page = int(request.GET.get('page', 1))
    query = request.GET.get('q', None)
    return process_polling(
        request=request,
        cache_key=f"films_page_{page}_query_{query}" if query else f"films_page_{page}",
        find_film_func=find_and_populate_paginated_all_film
    )


@swagger_auto_schema(
    operation_summary="Polling search bought film",
    operation_description="Find Bought film by search query or page. Will response when new data is available.",
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Search for bought films by title and director"),
        openapi.Parameter('Page', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Get bought films in certain page")
    ],
    responses={
        200: FilmResponse,
        204: FilmResponse,
    },
    method="GET"
)
@api_view(['GET'])
@protected
def bought_film_polling(request: APIRequest, *args, **kwargs):
    page = int(request.GET.get('page', 1))
    query = request.GET.get('q', None)
    return process_polling(
        request=request,
        cache_key=f"user_{request.user.id}_bought_films_page_{page}_query_{query}" if query else f"user_{request.user.id}_bought_films_page_{page}",
        find_film_func=find_and_populate_paginated_bought_film
    )


@swagger_auto_schema(
    operation_summary="Polling search wishlist film",
    operation_description="Find Wishlist film by search query or page. Will response when new data is available.",
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Search for wishlisted films by title and director"),
        openapi.Parameter('Page', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Get wishlisted films in certain page")
    ],
    responses={
        200: FilmResponse,
        204: FilmResponse,
    },
    method="GET"
)
@api_view(['GET'])
@protected
def wishlist_film_polling(request: APIRequest, *args, **kwargs):
    page = int(request.GET.get('page', 1))
    query = request.GET.get('q', None)
    return process_polling(
        request=request,
        cache_key=f"user_{request.user.id}_wishlist_films_page_{page}_query_{query}" if query else f"user_{request.user.id}_wishlist_films_page_{page}",
        find_film_func=find_and_populate_paginated_wishlist_film
    )





@swagger_auto_schema(
    operation_summary="Polling get film details",
    operation_description="Will response when new data is available.",
    responses={
        200: FilmDetailResponse,
        204: FilmDetailResponse,
    },
    method="GET"
)
@api_view(['GET'])
@protected
def film_details(request: APIRequest, id: int, *args, **kwargs):
    film = None
    try: film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return APIResponse(data=None, status=status.HTTP_404_NOT_FOUND)

    return process_polling(
        request=request,
        cache_key = f"film_{id}",
        find_film_func=lambda req, data: populate_film_details(req, data, film)
    )



@swagger_auto_schema(
    operation_summary="Polling get film reviews",
    operation_description="Find film reviews by page. Will response when new data is available.",
    responses={
        200: FilmResponse,
        204: FilmResponse,
    },
    method="GET"
)
@api_view(['GET'])
@protected
def reviews(request: APIRequest, id: int, *args, **kwargs):
    page = int(request.GET.get('page', 1))
    film = None
    try: film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return APIResponse(data=None, status=status.HTTP_404_NOT_FOUND)
    return process_polling(
        request=request,
        cache_key = f"reviews_film_{id}_page_{page}",
        find_film_func=lambda req, data: find_and_populate_paginated_film_review(req, data, film)
    )
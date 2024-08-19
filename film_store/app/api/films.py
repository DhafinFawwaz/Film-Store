from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from app.api.api_response import APIResponse, APIResponseMissingIDError
from app.models import Film, Genre
from app.serializers import FilmRequestSerializer, GenreSerializer, FilmResponseSerializer
from typing import List
from app.api.route_decorator import protected, admin_only, public
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from app.models import GeneralUser
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.api.swagger.film_schemas import FilmResponse, FilmFormParameters, FilmDetailResponse, FilmFormPutParameters
from app.api.swagger.api_response_schema import APIErrorResponse
from django.db.models import Q
from app.queries.film import find_and_populate_paginated_all_film_query_only
from django.core.cache import cache


class APIFilm(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = []
    authentication_classes = []

    def create_black_image():
        img = Image.new('RGB', (1, 1), color='black')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue(), 'black.png')

    # /films
    @swagger_auto_schema(
        operation_summary="Upload a new film",
        operation_description="A new film will be uploaded to the database and the response will contain the films url instead of the binary file",

        manual_parameters=FilmFormParameters,
        responses={
            201: FilmDetailResponse,
            400: APIErrorResponse,
            401: APIErrorResponse,
        },
        
    )
    @admin_only
    def post(self, request: Request, *args, **kwargs):
        film = FilmRequestSerializer(data=request.data)
        if not film.is_valid():
            return APIResponse().error(film.errors).set_status(status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("video") is None:
            return APIResponse().error("video is required").set_status(status.HTTP_400_BAD_REQUEST)

        cover_image = request.FILES.get("cover_image", None)
        if not cover_image:
            cover_image = APIFilm.create_black_image()
            cover_image.name = f'{request.data.get("title")}-{cover_image.name}'


        new_film = Film(
            title = request.data.get("title"),
            description = request.data.get("description"),
            director = request.data.get("director"),
            release_year = request.data.get("release_year"),
            price = request.data.get("price"),
            duration = request.data.get("duration"),
            video = request.data.get("video"),
            cover_image = cover_image,
        )
            

        new_film.save()

        genre_list = request.POST.getlist("genre")
        for genre_name in genre_list:
            genre = Genre.objects.get_or_create(name=genre_name)
            new_film.genre.add(genre[0])

        new_film.save()


        res = FilmResponseSerializer(new_film)

        return APIResponse(res.data).set_status(status.HTTP_201_CREATED)

    # /films
    @swagger_auto_schema(
        operation_summary="Get all films",
        operation_description="Query parameter 'q' can be used to search for films by title (case-insensitive)",
        manual_parameters=[openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Search for films by title and director")],
        responses={
            200: FilmResponse,
            400: APIErrorResponse,
            401: APIErrorResponse,
        },
        
    )
    @admin_only
    def get(self, request: Request, *args, **kwargs):
        context = {}
        find_and_populate_paginated_all_film_query_only(request, context)
        films = context['films']

        # prefix host to video_url and cover_image_url if not using Supabase
        if os.getenv("SUPABASE_KEY") is None:
            for film in films:
                film["video_url"] = request.build_absolute_uri(film["video_url"])
                if film["cover_image_url"] is not None:
                    film["cover_image_url"] = request.build_absolute_uri(film["cover_image_url"])

        return APIResponse(films)
        

class APIFilmDetail(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = []
    authentication_classes = []
    
    # /films/:id 
    @swagger_auto_schema(
        operation_summary="Get a film details by ID",
        operation_description="the id in the url is the film's ID primary key",
        responses={
            200: FilmDetailResponse,
            400: APIErrorResponse,
            401: APIErrorResponse,
        },
        
    )
    @public
    def get(self, request: Request, id: int = None, *args, **kwargs):
        if id is None: return APIResponseMissingIDError()
        try:
            film = Film.objects.get(id=id)
            film_serializer = FilmResponseSerializer(film)

            return APIResponse(film_serializer.data)
        except Film.DoesNotExist:
            return APIResponse().error("Film with id = "+ id +" not found").set_status(status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # /films/:id
    @swagger_auto_schema(
        operation_summary="Update a film",
        operation_description="The film data will be updated in the database and the response will contain the films url instead of the binary file",

        manual_parameters=FilmFormPutParameters,
        responses={
            201: FilmDetailResponse,
            400: APIErrorResponse,
            401: APIErrorResponse,
        },
    )
    @admin_only
    def put(self, request: Request, id: int = None, *args, **kwargs):
        try:
            film = Film.objects.get(id=id)
            film.title = request.data.get("title")
            film.description = request.data.get("description")
            film.director = request.data.get("director")
            film.release_year = request.data.get("release_year")
            film.price = request.data.get("price")
            film.duration = request.data.get("duration")

            
            video = request.data.get("video") # binary file, jika null artinya tidak berubah
            cover_image = request.data.get("cover_image") # binary file, jika null artinya tidak berubah

            if video is not None:
                film.video = video  
            if cover_image is not None:
                film.cover_image = cover_image
            film.save()

            # update genre
            genre_list = request.POST.getlist("genre")
            film.genre.clear()
            for genre_name in genre_list:
                genre = Genre.objects.get_or_create(name=genre_name)
                film.genre.add(genre[0])

            film.save()

            film_serializer = FilmResponseSerializer(film)
            return APIResponse(film_serializer.data)
            
        
        except Film.DoesNotExist:
            return APIResponse().error("Film with id = "+ id +" not found").set_status(status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /films/:id
    @swagger_auto_schema(
        operation_summary="Delete a film",
        operation_description="A new film will be uploaded to the database and the response will contain the films url instead of the binary file",

        manual_parameters=FilmFormPutParameters,
        responses={
            201: FilmDetailResponse,
            400: APIErrorResponse,
            401: APIErrorResponse,
        },
    )
    @admin_only
    def delete(self, request: Request, id: int = None, *args, **kwargs):
        try:
            film = Film.objects.get(id=id)
            film_serializer = FilmResponseSerializer(film)
            res = film_serializer.data # must be done before delete
            film.delete()
            return APIResponse(res)

        except Film.DoesNotExist:
            return APIResponse().error("Film with id = "+ id +" not found").set_status(status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

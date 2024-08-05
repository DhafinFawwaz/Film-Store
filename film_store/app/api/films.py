from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from app.api.api_response import APIResponse
from app.models import Film, Genre
from app.serializers import FilmRequestSerializer, GenreSerializer, FilmResponseSerializer
from typing import List
from app.api.protected import protected
import datetime

class APIFilm(APIView):

    # /films
    @protected
    def post(self, request: Request, *args, **kwargs):

        film = FilmRequestSerializer(data=request.data)
        if not film.is_valid():
            return APIResponse().error(film.errors).set_status(status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("video") is None:
            return APIResponse().error("video is required").set_status(status.HTTP_400_BAD_REQUEST)

        new_film = Film(
            title = request.data.get("title"),
            description = request.data.get("description"),
            director = request.data.get("director"),
            release_year = request.data.get("release_year"),
            price = request.data.get("price"),
            duration = request.data.get("duration"),
            video = request.data.get("video"),
            cover_image = request.data.get("cover_image"),
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
    @protected
    def get(self, request: Request, *args, **kwargs):

        film_list = Film.objects.all()
        film_serializer = FilmResponseSerializer(film_list, many=True)

        # prefix host to video_url and cover_image_url
        # change this if we're going to use cloud storage
        for film in film_serializer.data:
            film["video_url"] = request.build_absolute_uri(film["video_url"])
            if film["cover_image_url"] is not None:
                film["cover_image_url"] = request.build_absolute_uri(film["cover_image_url"])

        return APIResponse(film_serializer.data)
        

class APIFilmDetail(APIView):
    
    # /films/:id 
    @protected
    def get(self, request: Request, id, *args, **kwargs):
        print("=====================")
        # id = kwargs.get("id")
        # if id is None: return APIResponse().error("id is required")

        # film = Film.objects.get(id=id)
        # film_serializer = FilmResponseSerializer(film)

        # return APIResponse(film_serializer.data)

    # /films/:id
    @protected
    def put(self, request, *args, **kwargs):
        print("--------------------")
        id = kwargs["id"]
        if id is None: return APIResponse().error("id is required")

        title = request.data.get("title")
        description = request.data.get("description")
        director = request.data.get("director")
        release_year = request.data.get("release_year")
        genre = request.data.get("genre")
        price = request.data.get("price")
        duration = request.data.get("duration") # dalam detik
        video = request.data.get("video") # binary file, jika null artinya tidak berubah
        cover_image = request.data.get("cover_image") # binary file, jika null artinya tidak berubah

        return APIResponse({
           "id": "1",
           "title": "string",
           "description": "string",
           "director": "string",
           "release_year": 2020,
           "genre": ["string", "string2"],
           "price": 1000,
           "duration": 100,
           "video_url": "string",
           "cover_image_url": "string", # | null
           "created_at": "2020-01-01T00:00:00Z",
           "updated_at": "2020-01-01T00:00:00Z",
        })
    
    # /films/:id
    @protected
    def delete(self, request, *args, **kwargs):
        id = kwargs["id"]
        if id is None: return APIResponse().error("id is required")

        return APIResponse({
           "id": "1",
           "title": "string",
           "description": "string",
           "director": "string",
           "release_year": 2020,
           "genre": ["string", "string2"],
           "video_url": "string",
           "created_at": "2020-01-01T00:00:00Z",
           "updated_at": "2020-01-01T00:00:00Z",
        })
    

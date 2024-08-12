from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from app.api.api_response import APIResponse, APIResponseMissingIDError
from app.models import Film, Genre
from app.serializers import FilmRequestSerializer, GenreSerializer, FilmResponseSerializer
from typing import List
from app.api.route_decorator import protected
from rest_framework.decorators import api_view
from app.models import GeneralUser
import os

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

        q = request.GET.get("q")
        film_list = []
        
        if q is not None:
            film_list = Film.objects.filter(title__icontains=q)
        else:
            film_list = Film.objects.all()

        film_serializer = FilmResponseSerializer(film_list, many=True)

        # prefix host to video_url and cover_image_url if not using Supabase
        if os.getenv("SUPABASE_KEY") is None:
            for film in film_serializer.data:
                film["video_url"] = request.build_absolute_uri(film["video_url"])
                if film["cover_image_url"] is not None:
                    film["cover_image_url"] = request.build_absolute_uri(film["cover_image_url"])

        return APIResponse(film_serializer.data)
        

class APIFilmDetail(APIView):
    
    # /films/:id 
    @protected
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
    @protected
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
    @protected
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

    
# /films/:id/buy
@api_view(['POST'])
@protected
def buy_film(request: Request, id: int = None, *args, **kwargs):
    try:
        film = Film.objects.get(id=id)
        user: GeneralUser = request.user
        if user.balance < film.price:
            return APIResponse().error("Insufficient balance").set_status(status.HTTP_400_BAD_REQUEST)
        
        user.balance -= film.price
        user.save()

        return APIResponse(film)
    
    except Film.DoesNotExist:
        return APIResponse().error("Film with id = "+ id +" not found").set_status(status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# /films/bought
@api_view(['GET'])
@protected
def get_bought_films(request: Request, *args, **kwargs):
    try:
        user: GeneralUser = request.user
        film_list = user.bought_films.all()
        film_serializer = FilmResponseSerializer(film_list, many=True)
        return APIResponse(film_serializer.data)
    
    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

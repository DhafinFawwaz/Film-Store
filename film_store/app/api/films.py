from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from app.api.api_response import APIResponse
from rest_framework.decorators import api_view


class Film(APIView):

    # /films
    def post(self, request, *args, **kwargs):
        return APIResponse({
           "id": "string",
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

    # /films
    def get(self, request, *args, **kwargs):
        return APIResponse([
            {
                "id": "1",
                "title": "string",
                "director": "string",
                "release_year": 2020,
                "price": 1000,
                "genre": ["string", "string2"],
                "duration": 100,
                "cover_image_url": "string", # | null
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": "2020-01-01T00:00:00Z",
            },
        ])
        

class FilmDetail(APIView):
    
    # /films/:id 
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id is None: return APIResponse().error("id is required")

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
    def put(self, request, *args, **kwargs):
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
    

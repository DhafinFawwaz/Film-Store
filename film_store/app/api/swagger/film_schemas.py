
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.api.swagger.api_response_schema import APIResponseSchema

FilmFormParameters = [
    openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="The title of the film"),
    openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="A brief description of the film"),
    openapi.Parameter('director', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="The director of the film"),
    openapi.Parameter('release_year', openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True, description="The year the film was released"),
    openapi.Parameter('genre', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), required=True, description="A list of genres"),
    openapi.Parameter('price', openapi.IN_FORM, type=openapi.TYPE_NUMBER, required=True, description="The price of the film"),
    openapi.Parameter('duration', openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True, description="In seconds"),
    openapi.Parameter('video', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description="The video file"),
    openapi.Parameter('cover_image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False, description="The cover image of the film"),
]

FilmFormPutParameters = [
    openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="The title of the film"),
    openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="A brief description of the film"),
    openapi.Parameter('director', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="The director of the film"),
    openapi.Parameter('release_year', openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True, description="The year the film was released"),
    openapi.Parameter('genre', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), required=True, description="A list of genres"),
    openapi.Parameter('price', openapi.IN_FORM, type=openapi.TYPE_NUMBER, required=True, description="The price of the film"),
    openapi.Parameter('duration', openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True, description="In seconds"),
    openapi.Parameter('video', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False, description="The video file. If not provided, the video will not be updated"),
    openapi.Parameter('cover_image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False, description="The cover image of the film. If not provided, the cover image will not be updated"),
]

FilmResponseSchema = APIResponseSchema.copy()
FilmResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'id': openapi.Schema(type=openapi.TYPE_STRING, description="The ID of the film"),
    'title': openapi.Schema(type=openapi.TYPE_STRING, description="The title of the film"),
    # 'description': openapi.Schema(type=openapi.TYPE_STRING, description="A brief description of the film"),
    'director': openapi.Schema(type=openapi.TYPE_STRING, description="The director of the film"),
    'release_year': openapi.Schema(type=openapi.TYPE_INTEGER, description="The year the film was released"),
    'genre': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="A list of genres"),
    'price': openapi.Schema(type=openapi.TYPE_NUMBER, description="The price of the film"),
    'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="In seconds"),
    # 'video_url': openapi.Schema(type=openapi.TYPE_STRING, description="The URL to the video file"),
    'cover_image_url': openapi.Schema(type=openapi.TYPE_STRING, description="The URL to the cover image of the film"),
    'created_at': openapi.Schema(type=openapi.TYPE_STRING, description="The date the film was created"),
    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description="The date the film was last updated"),
    
})

FilmResponse = openapi.Schema(
    title='Film Response',
    type=openapi.TYPE_OBJECT,
    properties=FilmResponseSchema
)


# for some reasong using either dict.copy() directly to the .properties then use .update, also updates the original dict. Same thing happens with deepcopy. So let's just create a whole new dict
FilmDetailResponseSchema = APIResponseSchema.copy()
FilmDetailResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'id': openapi.Schema(type=openapi.TYPE_STRING, description="The ID of the film"),
    'title': openapi.Schema(type=openapi.TYPE_STRING, description="The title of the film"),
    'description': openapi.Schema(type=openapi.TYPE_STRING, description="A brief description of the film"),
    'director': openapi.Schema(type=openapi.TYPE_STRING, description="The director of the film"),
    'release_year': openapi.Schema(type=openapi.TYPE_INTEGER, description="The year the film was released"),
    'genre': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="A list of genres"),
    'price': openapi.Schema(type=openapi.TYPE_NUMBER, description="The price of the film"),
    'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="In seconds"),
    'video_url': openapi.Schema(type=openapi.TYPE_STRING, description="The URL to the video file"),
    'cover_image_url': openapi.Schema(type=openapi.TYPE_STRING, x_nullable=True, description="The URL to the cover image of the film"),
    'created_at': openapi.Schema(type=openapi.TYPE_STRING, description="The date the film was created"),
    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description="The date the film was last updated"),
    
})
FilmDetailResponse = openapi.Schema(
    title='Film Response Detail',
    type=openapi.TYPE_OBJECT,
    properties=FilmDetailResponseSchema
)

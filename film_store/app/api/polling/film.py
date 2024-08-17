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
from app.auth.jwt import JWT
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, authentication_classes
from django.shortcuts import redirect
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from app.api.swagger.auth_schemas import LoginFormBody, RegisterFormBody, LoginResponse, RegisterResponse, LogoutResponseSchema, SelfResponse, UsersResponse
from app.api.swagger.api_response_schema import APIErrorResponse
from time import sleep
from django.core.cache import cache
from datetime import datetime

# /logout
@swagger_auto_schema(
    operation_summary="",
    operation_description="",
    request_body=LogoutResponseSchema,
    responses={
        200: UsersResponse,
    },
    method="GET"
)
@api_view(['GET'])
@protected
def home(request: Request, *args, **kwargs):
    return APIResponse(data={"message": "test1"}, status=status.HTTP_200_OK)
    current_film_update_at = cache.get("film_update_at")
    if current_film_update_at is None:
        cache.set("film_update_at", datetime.now())
        current_film_update_at = cache.get("film_update_at")

    while True:
        sleep(1)
        cached_film_update_at = cache.get("film_update_at")
        print()
        print(f"current_film_update_at: {current_film_update_at}")
        print(f"cached_film_update_at: {cached_film_update_at}")
        print(type(current_film_update_at))
        print(type(cached_film_update_at))
        if cached_film_update_at != current_film_update_at:
            break

    print("break")

    return APIResponse(data={"message": "test1"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def test2(request: Request, *args, **kwargs):
    return APIResponse(data={"message": "test1"}, status=status.HTTP_200_OK)
    cache.set("film_update_at", datetime.now())
    return APIResponse(data={"message": "test1"}, status=status.HTTP_200_OK)



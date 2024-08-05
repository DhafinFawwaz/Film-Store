from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from app.api.api_response import APIResponse
from app.models import GeneralUser
from app.serializers import GeneralUserSerializer
from django.db.utils import IntegrityError
from rest_framework.serializers import ValidationError

@api_view(['POST'])
def login(request, *args, **kwargs):
    try:
        user = GeneralUser.objects.get(username = request.data.get('username'))
        if user.check_password(request.data.get('password')):
            refresh = RefreshToken.for_user(user)
            return APIResponse({
                "username": user.username,
                "token": str(refresh.access_token),
            })
        else:
            return APIResponse().error("Wrong password").set_status(status.HTTP_401_UNAUTHORIZED)
    except GeneralUser.DoesNotExist:
        return APIResponse().error("User with username =", user,"does not exist").set_status(status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def self(request, *args, **kwargs):
    auth_str = request.META.get('HTTP_AUTHORIZATION')
    if not auth_str:
        return APIResponse().error("No token provided").set_status(status.HTTP_401_UNAUTHORIZED)
    
    split_auth = auth_str.split(' ')
    if len(split_auth) != 2:
        return APIResponse().error("Invalid token").set_status(status.HTTP_401_UNAUTHORIZED)

    # Recheck token in database

    user = GeneralUserSerializer(request.user).data
    user["token"] = split_auth[1]

    return APIResponse(user)
    

@api_view(['POST'])
def register(request, *args, **kwargs):
    try:
        request.data["balance"] = 0
        request.data["is_active"] = True
        
        new_user_serializer = GeneralUserSerializer(data=request.data)
        if new_user_serializer.is_valid():
            new_user_serializer.save()
            return APIResponse(new_user_serializer.data)
        else:
            return APIResponse().error(new_user_serializer.errors).set_status(status.HTTP_400_BAD_REQUEST)
        
    except IntegrityError as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
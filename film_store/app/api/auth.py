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

class APILogin(APIView):
    permission_classes = []
    authentication_classes = []

    # /login
    @public
    def post(self, request: Request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = GeneralUser.objects.get(username = username)

            if user.check_password(password):
                token = JWT.encode(user)
                res = APIResponse({
                    "username": user.username,
                    "token": str(token),
                }).set_cookie(
                    key = "token", 
                    value = token,
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = True,
                    httponly = True,
                    samesite = False
                )
                return res
            else:
                return APIResponse().error("Wrong password").set_status(status.HTTP_401_UNAUTHORIZED)
        except GeneralUser.DoesNotExist:
            return APIResponse().error("Username "+ username +" does not exist").set_status(status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # /login
    @public
    def get(self, request: Request, *args, **kwargs): return redirect('/signin')
        

class APIRegister(APIView):
    permission_classes = []
    authentication_classes = []

    # /register
    @public
    def post(self, request: APIRequest, *args, **kwargs) -> APIResponse:
        try: request.data._mutable=True
        except Exception as e: pass

        try:
            request.data["balance"] = 0
            request.data["is_active"] = True
            
            new_user_serializer = GeneralUserSerializer(data=request.data)
            if new_user_serializer.is_valid():
                new_user_serializer.save()
                return APIResponse(new_user_serializer.data).set_status(status.HTTP_201_CREATED)
            else:
                return APIResponse().error(new_user_serializer.errors).set_status(status.HTTP_400_BAD_REQUEST)
            
        except IntegrityError as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /register
    @public
    def get(self, request: APIRequest, *args, **kwargs) -> APIResponse: return redirect('/signup')

@api_view(['GET'])
@protected
def self(request: APIRequest, *args, **kwargs):
    user = GeneralUserSerializer(request.user).data
    user["token"] = request.token
    return APIResponse(user)


@api_view(['POST'])
@protected
def logout(request: Request, *args, **kwargs):
    user = GeneralUserSerializer(request.user).data
    res = APIResponse(user).delete_cookie("csrftoken").delete_cookie("token")
    return res


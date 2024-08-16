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

class APILogin(APIView):
    permission_classes = []
    authentication_classes = []

    # /login
    @swagger_auto_schema(
        operation_summary="Login a user",
        operation_description="The user will be logged in and a token will be returned",
        request_body=LoginFormBody,
        responses={
            200: LoginResponse,
            400: APIErrorResponse,
        },
    )
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
                    secure = False,
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

    # /login, redirected for views
    @swagger_auto_schema(auto_schema=None)
    @public
    def get(self, request: Request, *args, **kwargs): return redirect('/signin')
        

class APIRegister(APIView):
    permission_classes = []
    authentication_classes = []

    # /register
    @swagger_auto_schema(
        operation_summary="Register a user",
        operation_description="The user will be registered and a token will be returned",
        request_body=RegisterFormBody,
        responses={
            201: RegisterResponse,
            400: APIErrorResponse,
        },
    )
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
    
    # /register, redirected for views
    @swagger_auto_schema(auto_schema=None)
    @public
    def get(self, request: APIRequest, *args, **kwargs) -> APIResponse: return redirect('/signup')

# /self
@swagger_auto_schema(
    operation_summary="Get current user data",
    operation_description="Get the current user data by the auth token",
    responses={
        200: SelfResponse,
        400: APIErrorResponse,
        401: APIErrorResponse,
    },
    method="GET"
)
@api_view(['GET'])
@protected
def self(request: APIRequest, *args, **kwargs):
    user = GeneralUserSerializer(request.user).data
    user["token"] = request.token
    return APIResponse(user)

# /logout
@swagger_auto_schema(
    operation_summary="Logout user",
    operation_description="Logout the user and delete the token",
    request_body=LogoutResponseSchema,
    responses={
        200: UsersResponse,
        400: APIErrorResponse,
        401: APIErrorResponse,
    },
    method="POST"
)
@api_view(['POST'])
@protected
def logout(request: Request, *args, **kwargs):
    user = GeneralUserSerializer(request.user).data
    res = APIResponse(user).delete_cookie("csrftoken").delete_cookie("token")
    return res


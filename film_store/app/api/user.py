from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view
from app.api.api_response import APIResponse, APIResponseMissingIDError
from app.models import GeneralUser
from app.serializers import GeneralUserSerializer
from app.api.route_decorator import protected, admin_only
from drf_yasg.utils import swagger_auto_schema
from app.api.swagger.auth_schemas import UsersResponse, UserDetailResponse, UserBalanceResponse, UserDeleteResponse
from drf_yasg import openapi
from app.api.swagger.api_response_schema import APIErrorResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from decimal import Decimal


@swagger_auto_schema(
    operation_summary="Get all users",
    operation_description="Get all users in the database",
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, description="Search for a user by username", type=openapi.TYPE_STRING),
    ],
    responses={
        200: UsersResponse,
        400: APIErrorResponse,
        401: APIErrorResponse,
    },
    method="GET"
)
@api_view(['GET']) # /users?q
@admin_only
def get_all_users(request: Request, *args, **kwargs):
    try:
        q = request.query_params.get("q")
        
        if q is None:
            all_user = GeneralUser.objects.all()
            all_user_dict = GeneralUserSerializer(all_user, many=True)
            return APIResponse(all_user_dict.data)
        else:
            found_user = GeneralUser.objects.filter(username__icontains=q)
            found_user_dict = GeneralUserSerializer(found_user, many=True)
            return APIResponse(found_user_dict.data)
        
    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@swagger_auto_schema(
    operation_summary="Modify a user's balance",
    operation_description="Change a user's balance by ID",
    responses={
        200: UserBalanceResponse,
        400: APIErrorResponse,
        401: APIErrorResponse,
    },
    method="POST"
)
@api_view(['POST']) # /users/:id/balance
@admin_only
def increment_user_balance_by_id(request: Request, id: int = None, *args, **kwargs):
    try:
        increment = request.data.get("increment")
        if increment is None: return APIResponse().error("increment is required in body").set_status(status.HTTP_400_BAD_REQUEST)

        user = GeneralUser.objects.get(id=id)
        user.balance += Decimal(increment)
        user.save()

        user_dict = GeneralUserSerializer(user)
        return APIResponse(user_dict.data)
    
    except GeneralUser.DoesNotExist as e:
        return APIResponse().error("User with id = "+ id +" does not exist").set_status(status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersAPI(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = []
    authentication_classes = []

    # /users/:id
    @swagger_auto_schema(
        operation_summary="Delete a user by ID",
        operation_description="Delete a user by ID",
        responses={
            200: UserDetailResponse,
            400: APIErrorResponse,
            401: APIErrorResponse,
        },
    )
    @admin_only
    def delete(self, request: Request, id: int = None, *args, **kwargs):
        try:
            user = GeneralUser.objects.get(id=id)
            user_dict = GeneralUserSerializer(user)
            res = user_dict.data # must be done before delete
            user.delete()

            return APIResponse(res)
        
        except GeneralUser.DoesNotExist as e:
            return APIResponse().error("User with id = "+ id +" does not exist").set_status(status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

     # /users/:id
    
    # /users/:id
    @swagger_auto_schema(
        operation_summary="Get user by ID",
        operation_description="Get user by ID",
        responses={
            200: UserDetailResponse,
            400: APIErrorResponse,
            401: APIErrorResponse,
        },
    )
    @admin_only
    def get(self, request: Request, id: int = None, *args, **kwargs):
        try:
            user = GeneralUser.objects.get(id=id)
            user_dict = GeneralUserSerializer(user)

            return APIResponse(user_dict.data)
        
        except GeneralUser.DoesNotExist as e:
            return APIResponse().error("User with id = "+ id +" does not exist").set_status(status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

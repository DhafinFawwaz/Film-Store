from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view
from app.api.api_response import APIResponse, APIResponseMissingIDError
from app.models import GeneralUser
from app.serializers import GeneralUserSerializer
from app.api.protected import protected, admin_only

@api_view(['GET']) # /users?q, admin only
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
    

@api_view(['GET']) # /user/:id
@admin_only
def get_user_by_id(request: Request, id: int = None, *args, **kwargs):
    try:
        user = GeneralUser.objects.get(id=id)
        user_dict = GeneralUserSerializer(user)

        return APIResponse(user_dict.data)
    
    except GeneralUser.DoesNotExist as e:
        return APIResponse().error("User with id = "+ id +" does not exist").set_status(status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST']) # /users/:id/balance
@admin_only
def increment_user_balance_by_id(request: Request, id: int = None, *args, **kwargs):
    try:
        increment = request.data.get("increment")
        if increment is None: return APIResponse().error("increment is required in body").set_status(status.HTTP_400_BAD_REQUEST)

        user = GeneralUser.objects.get(id=id)
        user.balance += increment
        user.save()

        user_dict = GeneralUserSerializer(user)
        return APIResponse(user_dict.data)
    
    except GeneralUser.DoesNotExist as e:
        return APIResponse().error("User with id = "+ id +" does not exist").set_status(status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE']) # /users/:id
@admin_only
def delete_user_by_id(request: Request, id: int = None, *args, **kwargs):
    try:
        user = GeneralUser.objects.get(id=id)
        user_dict = GeneralUserSerializer(user)
        user.delete()

        return APIResponse(user_dict.data)
    
    except GeneralUser.DoesNotExist as e:
        return APIResponse().error("User with id = "+ id +" does not exist").set_status(status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return APIResponse().error(str(e)).set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

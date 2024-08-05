
from app.api.api_response import APIResponse
from rest_framework import status
from functools import wraps
from rest_framework.request import Request
from app.models import GeneralUser

def protected(view_func):
    @wraps(view_func)
    def _wrapped_view(*args):
        print("Protected view called")
        print(args)
        request = None
        for req in args:
            if isinstance(req, Request):
                request = req
                break
        if not request:
            raise Exception("No request object found")

        auth_str = request.headers.get('Authorization')
        if not auth_str:
            return APIResponse().error("No token provided").set_status(status.HTTP_401_UNAUTHORIZED)
        
        split_auth = auth_str.split(' ')
        if len(split_auth) != 2:
            return APIResponse().error("Invalid token").set_status(status.HTTP_401_UNAUTHORIZED)
        
        if split_auth[0].lower() != 'bearer':
            return APIResponse().error("Invalid token prefix").set_status(status.HTTP_401_UNAUTHORIZED)
        
        try:
            user = GeneralUser.objects.get(username=request.user.username)
        except GeneralUser.DoesNotExist:
            return APIResponse().error("User does not exist").set_status(status.HTTP_401_UNAUTHORIZED)
        
        return view_func(*args)
    
    return _wrapped_view

def admin_only(view_func):
    @wraps(view_func)
    @protected
    def _wrapped_view(request, *args, **kwargs):
        if request.user.username != 'admin':
            return APIResponse().error("Unauthorized").set_status(status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

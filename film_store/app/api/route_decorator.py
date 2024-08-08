
from app.api.api_response import APIResponse
from rest_framework import status
from functools import wraps
from rest_framework.request import Request
from app.models import GeneralUser
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from typing import Tuple

def populate_user_from_request(request: Request) -> GeneralUser:
    user = None
    token = request.COOKIES.get('token')
    error_message = "No token provided"

    # Case: HttpOnly Cookie Token
    if token:
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        print("HttpOnly Cookie Token:", token)
        user = JWTAuthentication().authenticate(request)
        if user: 
            request.user = user[0]
            request.token = token
        else: error_message = "Invalid token"

    # Case: Authorization Header Token or HttpOnly Cookie Token failed
    if not user:
        token = request.headers.get('Authorization')
        if not token: raise Exception(error_message)
        print("Authorization:", token)    
        user = JWTAuthentication().authenticate(request)
        if user: 
            request.user = user[0]
            request.token = token
        else: raise Exception("Invalid token")

def protected(view_func):
    @wraps(view_func)
    @authentication_classes([])
    def _wrapped_view(*args, **kwargs):
        request = None
        for req in args:
            if isinstance(req, Request):
                request = req
                break
        if not request:
            raise Exception("No request object found")
        
        try:
            populate_user_from_request(request)
        except Exception as e:
            return APIResponse().error(str(e)).set_status(status.HTTP_401_UNAUTHORIZED)
        
        return view_func(*args, **kwargs)
    
    return _wrapped_view

def admin_only(view_func):
    @wraps(view_func)
    @protected
    def _wrapped_view(request, *args, **kwargs):
        if request.user.username != 'admin':
            return APIResponse().error("Unauthorized").set_status(status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def public(view_func):
    @wraps(view_func)
    @authentication_classes([])
    def _wrapped_view(*args, **kwargs):
        request = None
        for req in args:
            if isinstance(req, Request):
                request = req
                break
        if not request:
            raise Exception("No request object found")

        try:
            populate_user_from_request(request)
        except Exception as e:
            request.user = None

        return view_func(*args, **kwargs)
    return _wrapped_view



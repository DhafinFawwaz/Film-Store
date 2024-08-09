
from rest_framework.request import Request
from app.models import GeneralUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from typing import Tuple
from django.core.handlers.wsgi import WSGIRequest
from app.auth.jwt import JWT
from app.api.api_request import APIRequest


# will raise exception if token is invalid or not provided
def populate_user_from_request(request: APIRequest) -> GeneralUser:
    user = None
    token = request.COOKIES.get('token')
    error_message = "No token provided"

    # Case: HttpOnly Cookie Token
    if token:
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        print(f"HttpOnly Cookie Token:\n{token}")
        user = JWT.authenticate(request)
        if user: 
            request.user = user
            request.token = token
        else: error_message = "Invalid token"

    # Case: Authorization Header Token or HttpOnly Cookie Token failed
    if not user:
        token = request.headers.get('Authorization')
        if not token: raise Exception(error_message)
        print(f"Authorization:\n{token}")    
        user = JWT.authenticate(request)
        if user: 
            request.user = user
            request.token = token
        else: raise Exception("Invalid token")

# will raise exception if request is not found in args
def extract_request_from_args(args: Tuple) -> Request:
    request = None
    for req in args:
        if isinstance(req, Request) or isinstance(req, WSGIRequest):
            request = req
            break
    if not request:
        raise Exception("No request object found")
    return request

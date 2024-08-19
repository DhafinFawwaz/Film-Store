
from app.api.api_response import APIResponse
from rest_framework import status
from functools import wraps
from rest_framework.decorators import permission_classes, authentication_classes
from app.auth.auth import Auth
from app.auth.jwt import JWT
from rest_framework.views import APIView

def protected(view_func):
    @wraps(view_func)
    @authentication_classes([])
    def _wrapped_view(*args, **kwargs):
        request = Auth.extract_request_from_args(args)
        try: Auth.populate_user_from_request(request)
        except Exception as e: return APIResponse().error(str(e)).set_status(status.HTTP_401_UNAUTHORIZED)
        return view_func(*args, **kwargs)
    
    return _wrapped_view

def admin_only(view_func):
    @wraps(view_func)
    @protected
    def _wrapped_view(*args, **kwargs):
        print("admin_only")
        request = Auth.extract_request_from_args(args)
        if request.user.username != 'admin':
            return APIResponse().error("Unauthorized").set_status(status.HTTP_403_FORBIDDEN)
        return view_func(*args, **kwargs)
    return _wrapped_view


def public(view_func):
    @wraps(view_func)
    @authentication_classes([])
    @permission_classes([])
    def _wrapped_view(*args, **kwargs):
        print("public")
        request = Auth.extract_request_from_args(args)
        try: Auth.populate_user_from_request(request)
        except Exception as e: request.user = None
        return view_func(*args, **kwargs)
    
    return _wrapped_view



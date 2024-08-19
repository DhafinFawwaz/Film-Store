
from functools import wraps
from app.auth.auth import Auth
from app.auth.jwt import JWT
from django.shortcuts import redirect
from django.contrib import messages
import time

def protected(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = Auth.extract_request_from_args(args)
        try: 
            Auth.populate_user_from_request(request)
        except Exception as e: 
            messages.info(request, "Please Login", "Please Login to gain full access to the website")
            return redirect('/signin')
        return view_func(*args, **kwargs)
    
    return _wrapped_view

def unauthorized(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = Auth.extract_request_from_args(args)
        try: 
            Auth.populate_user_from_request(request)
            messages.info(request, "You are already logged in", "Logout if you want to login with another account")
            return redirect('/')
        except Exception as e: request.user = None
        return view_func(*args, **kwargs)
    
    return _wrapped_view

def public(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = Auth.extract_request_from_args(args)
        try: Auth.populate_user_from_request(request)
        except Exception as e: request.user = None
        return view_func(*args, **kwargs)
    
    return _wrapped_view


def timeit(message=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            if message: print(f"{message} took {total_time:.4f} seconds")
            else: print(f"{func.__name__} took {total_time:.4f} seconds")
            return result
        return wrapper
    return decorator

from functools import wraps
from app.auth.auth import populate_user_from_request, extract_request_from_args
from django.shortcuts import redirect

def protected(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = extract_request_from_args(args)
        try: 
            populate_user_from_request(request)
            print(f"User: {request.user}")
        except Exception as e: return redirect('/signin')
        return view_func(*args, **kwargs)
    
    return _wrapped_view

def public(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = extract_request_from_args(args)
        try: 
            populate_user_from_request(request)
            return redirect('/')
        except Exception as e: request.user = None
        return view_func(*args, **kwargs)
    
    return _wrapped_view


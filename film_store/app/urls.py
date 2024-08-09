from django.urls import path
from app.api import auth
from app.api import user
from app.api.films import APIFilm, APIFilmDetail
from app.api import seed
from .views import auth_views, film_views
from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_url(request: Request):
    if request.method == 'POST': return auth.login(request)
    elif request.method == 'GET': return auth_views.Login.as_view()(request)
    else: return HttpResponseNotAllowed(['GET', 'POST'])

def register_url(request: Request):
    if request.method == 'POST': return auth.register(request)
    elif request.method == 'GET': return auth_views.Register.as_view()(request)
    else: return HttpResponseNotAllowed(['GET', 'POST'])

def logout_url(request):
    if request.method == 'POST': return auth.logout(request)
    elif request.method == 'GET': return render(request, '404.html')
    else: return HttpResponseNotAllowed(['POST'])

urlpatterns = [

    # Views
    path('signup', auth_views.Register.as_view()),  # POST from views, return redirect('/login')
    path('signin', auth_views.Login.as_view()),     # POST from views, return redirect('/')
    path('signout', auth_views.Logout.as_view()),   # POST from views, return redirect('/login')
    path('profile', auth_views.Profile.as_view()),
    
    path('', film_views.Browse.as_view()),    
    path('wishlist', film_views.Wishlist.as_view()),
    path('review', film_views.Review.as_view()),
    path('bought', film_views.Bought.as_view()),
    path('details/<int:id>', film_views.Details.as_view()),



    # API
    path('register', register_url), # POST from REST API, return json | GET from views, return views
    path('login', login_url),       # POST from REST API, return json | GET from views, return views
    path('logout', logout_url),     # POST from REST API, return json | GET from views, return 404 page manually because django won't automatically return 404 page
    path('self', auth.self),

    path('users', user.get_all_users),
    path('user/<int:id>', user.get_user_by_id),
    path('users/<int:id>/balance', user.increment_user_balance_by_id),
    path('users/<int:id>', user.delete_user_by_id),

    path('films/<int:id>', APIFilmDetail.as_view()),
    path('films', APIFilm.as_view()),

    path('seed', seed.seed_db),


]
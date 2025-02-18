from django.urls import path
from app.api import auth
from app.api import user
from app.api.user import UsersAPI
from app.api.films import APIFilm, APIFilmDetail
from app.api.polling import film
from .views import auth_views, film_views
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def logout_url(request):
    if request.method == 'POST': return auth.logout(request)
    elif request.method == 'GET': return render(request, '404.html')
    else: return HttpResponseNotAllowed(['POST'])

urlpatterns = [

    # Views
    path('signup', auth_views.Register.as_view()),
    path('signin', auth_views.Login.as_view()),   
    path('signout', auth_views.Logout.as_view()), 
    path('profile', auth_views.Profile.as_view()),
    
    path('', film_views.Home.as_view()),    
    path('explore', film_views.Explore.as_view()),    
    path('wishlist', film_views.Wishlist.as_view()),
    path('bought', film_views.Bought.as_view()),
    path('details/<int:id>', film_views.Details.as_view()),
    path('details/<int:id>/buy', film_views.BuyFilm.as_view()),
    path('details/<int:id>/wish', film_views.WishlistFilm.as_view()),
    path('details/<int:id>/rate', film_views.Rate.as_view()),
    path('details/<int:id>/review', film_views.ReviewView.as_view()),
    path('details/<int:id>/watch', film_views.Watch.as_view()),


    # API
    path('register', auth.APIRegister.as_view()),
    path('login', auth.APILogin.as_view()),      
    path('logout', logout_url),    
    path('self', auth.self),

    path('users', user.get_all_users),
    path('users/<int:id>', UsersAPI.as_view()),
    path('users/<int:id>/balance', user.increment_user_balance_by_id),

    path('films/<int:id>', APIFilmDetail.as_view()),
    path('films', APIFilm.as_view()),
    
    
    # Polling API
    path('polling/film', film.film_polling),
    path('polling/wishlist', film.wishlist_film_polling),
    path('polling/bought', film.bought_film_polling),
    path('polling/details/<int:id>', film.film_details),
    path('polling/details/<int:id>/review', film.reviews),
]
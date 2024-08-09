from django.urls import path
from app.api import auth
from app.api import user
from app.api.films import APIFilm, APIFilmDetail
from app.api import seed
from . import views
from . import forms

urlpatterns = [
    # Views

    path('', views.Browse.as_view()),    
    path('wishlist', views.Wishlist.as_view()),
    path('profile', views.Profile.as_view()),
    path('review', views.Review.as_view()),
    path('bought', views.Bought.as_view()),
    path('details/<int:id>', views.Details.as_view()),
    path('signin', views.SignIn.as_view()),
    path('signup', views.SignUp.as_view()),



    # API
    path('login', auth.login),
    path('self', auth.self),
    path('register', auth.register),
    path('logout', auth.logout),

    path('users', user.get_all_users),
    path('user/<int:id>', user.get_user_by_id),
    path('users/<int:id>/balance', user.increment_user_balance_by_id),
    path('users/<int:id>', user.delete_user_by_id),

    path('films/<int:id>', APIFilmDetail.as_view()),
    path('films', APIFilm.as_view()),

    path('seed', seed.seed_db),


]
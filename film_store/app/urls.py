from django.urls import path
from app.api import auth
from app.api import user
from app.api.films import APIFilm, APIFilmDetail
from app.api import seed
from . import views

urlpatterns = [
    # Views

    path('home', views.Home.as_view()),    
    path('login', views.Login.as_view()),
    path('register', views.Register.as_view()),



    # API
    path('login', auth.login),
    path('self', auth.self),

    path('register', auth.register),

    path('users', user.get_all_users),
    path('user/<int:id>', user.get_user_by_id),
    path('users/<int:id>/balance', user.increment_user_balance_by_id),
    path('users/<int:id>', user.delete_user_by_id),

    path('films/<int:id>', APIFilmDetail.as_view()),
    path('films', APIFilm.as_view()),

    path('seed', seed.seed_db),


]
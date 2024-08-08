from typing import Any
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from app.models import GeneralUser, Film
from app.serializers import GeneralUserSerializer, FilmResponseSerializer
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from app.api.auth import register
from django.shortcuts import render
from django import forms
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm


class LoginForm():
    template_name = 'login.html'


class ProtectedView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/signin')
        return super().get(request, *args, **kwargs)

class PublicFormView(FormView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)
 


class Details(ProtectedView):
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film_id = kwargs['id']
        film = Film.objects.get(id=film_id)
        film = FilmResponseSerializer(film).data
        context['film'] = film
        return context

class Bought(ProtectedView):
    template_name = 'bought.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        films = user.bought_films.all()
        context['films'] = films
        return context

class Profile(ProtectedView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        user = GeneralUserSerializer(user).data
        context['user'] = user
        return context

class Browse(ProtectedView):
    template_name = 'browse.html'

    def get_recommendations(self, user):
        return Film.objects.all()[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'q' in self.request.GET:
            query = self.request.GET['q']
            films = Film.objects.filter(title__icontains=query)
            films = FilmResponseSerializer(films, many=True).data
            context['films'] = films
            return context

        films = Film.objects.all()
        films = FilmResponseSerializer(films, many=True).data
        context['films'] = films
        return context
    
    
class Review(ProtectedView):
    template_name = 'review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film_id = kwargs['id']

        film = Film.objects.get(id=film_id) # TODO: Handle exception
        film = FilmResponseSerializer(film).data 
        context['film'] = film

        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        context['user'] = user

        user_review = Review.objects.filter(film=film, user=user) # TODO: Handle case where user has not reviewed the film, or review text is null, or rating is null
        all_reviews = Review.objects.filter(film=film)
        context['user_review'] = user_review
        context['all_reviews'] = all_reviews
        return context

class Wishlist(ProtectedView):
    template_name = 'wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        films = user.wishlist_films.all()
        context['films'] = films
        return context
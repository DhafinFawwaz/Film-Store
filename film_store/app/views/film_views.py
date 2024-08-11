from app.models import GeneralUser, Film
from app.serializers import GeneralUserSerializer, FilmResponseSerializer
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from .. import forms
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from app.views.views_class import PublicView, ProtectedView
from app.utils import duration_to_format

class Browse(ProtectedView):
    template_name = 'browse/browse.html'

    def get_recommendations(self, user):
        return Film.objects.all()[:5]

    

    def get(self, request, *args, **kwargs):
        context = {}
        if 'q' in self.request.GET:
            query = self.request.GET['q']
            films = Film.objects.filter(title__icontains=query)
            films = FilmResponseSerializer(films, many=True).data
            context['films'] = films
            context['query'] = query
            return render(request, self.template_name, context)

        films = Film.objects.all()
        films = FilmResponseSerializer(films, many=True).data
        for film in films:
            film['duration'] = duration_to_format(film['duration'])

        context['films'] = films
        return render(request, self.template_name, context)

    

class Details(ProtectedView):
    template_name = 'details/details.html'

    def get(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        film = Film.objects.get(id=film_id)
        film = FilmResponseSerializer(film).data
        film['duration'] = duration_to_format(film['duration'])
        context['film'] = film
        context['balance_left_if_purchased'] = request.user.balance - film['price']

        # TODO: Check if purchased. If purchased, show watch button. If not, show purchase button.
        return render(request, self.template_name, context)
        

class Bought(ProtectedView):
    template_name = 'bought/bought.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        films = user.bought_films.all()
        context['films'] = films
        return render(request, self.template_name, context)


class Review(ProtectedView):
    template_name = 'review/review.html'

    def get(self, request, *args, **kwargs):
        context = {}
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

        return render(request, self.template_name, context)

class Wishlist(ProtectedView):
    template_name = 'wishlist/wishlist.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        films = user.wishlist_films.all()
        context['films'] = films
        return render(request, self.template_name, context)
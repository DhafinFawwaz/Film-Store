from typing import Any
from django.views.generic.base import TemplateView
from django.views import View
from django.views.generic import FormView
from app.models import GeneralUser, Film
from app.serializers import GeneralUserSerializer, FilmResponseSerializer
from app.api.auth import register
from django.shortcuts import render
from django import forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from . import forms
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from app.view_decorator import protected, public

class PublicView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, 'get'): self.get = public(self.get)
        if hasattr(self, 'post'): self.post = public(self.post)

class ProtectedView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, 'get'): self.get = protected(self.get)
        if hasattr(self, 'post'): self.post = protected(self.post)

class SignUp(PublicView):
    form_class = forms.RegisterForm
    template_name = "register.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form}) 
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        if not form.is_valid(): return render(request, 'register.html', {'form': form})
        
        user = form.save(commit=False)
        user.save()
        messages.success(request, 'You have signed up successfully.')
        return redirect('/signin')
        


class SignIn(PublicView):
    form_class = forms.LoginForm
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid(): return render(request, self.template_name, {"form": form})
        try:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = GeneralUser.objects.get(username = username)

            if not user.check_password(password):
                messages.error(request, "Wrong password")
                return render(request, self.template_name, {"form": form})
            else:
                messages.success(request, 'You have signed in successfully.')
                refresh = RefreshToken.for_user(user)
                res = redirect('/')
                res.set_cookie(
                    key = "token", 
                    value = refresh.access_token,
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = True,
                    httponly = True,
                    samesite = False
                )
                return res
        except GeneralUser.DoesNotExist:
            messages.error(request, "Username "+ username +" does not exist")
            return render(request, self.template_name, {"form": form})

        except Exception as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {"form": form})



class Browse(ProtectedView):
    template_name = 'browse.html'

    def get_recommendations(self, user):
        return Film.objects.all()[:5]

    def get(self, request, *args, **kwargs):
        context = {}
        if 'q' in self.request.GET:
            query = self.request.GET['q']
            films = Film.objects.filter(title__icontains=query)
            films = FilmResponseSerializer(films, many=True).data
            context['films'] = films
            return context

        films = Film.objects.all()
        films = FilmResponseSerializer(films, many=True).data
        context['films'] = films
        return render(request, self.template_name, context)

    

class Details(ProtectedView):
    template_name = 'details.html'

    def get(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        film = Film.objects.get(id=film_id)
        film = FilmResponseSerializer(film).data
        context['film'] = film
        return render(request, self.template_name, context)
        

class Bought(ProtectedView):
    template_name = 'bought.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        films = user.bought_films.all()
        context['films'] = films
        return render(request, self.template_name, context)

class Profile(ProtectedView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        user = GeneralUserSerializer(user).data
        context['user'] = user
        return render(request, self.template_name, context)

class Review(ProtectedView):
    template_name = 'review.html'

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
    template_name = 'wishlist.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        films = user.wishlist_films.all()
        context['films'] = films
        return render(request, self.template_name, context)
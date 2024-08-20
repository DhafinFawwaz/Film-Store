from app.models import GeneralUser
from app.serializers import GeneralUserSerializer
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from .. import forms
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from app.views.views_class import UnauthorizedView, ProtectedView
from django.http import HttpResponseNotAllowed
from app.auth.token import Token
from app.auth.auth import Auth
from app.auth.jwt import JWT


class Register(UnauthorizedView):
    form_class = forms.RegisterForm
    template_name = "register/register.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form}) 
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        if not form.is_valid(): 
            messages.error(request, "Failed to Register", "Please complete the form properly")
            return render(request, self.template_name, {'form': form})
        
        user = form.save(commit=False)
        user.save()
        messages.success(request, "Success", "You have registered successfully")
        return redirect('/signin')
        


class Login(UnauthorizedView):
    form_class = forms.LoginForm
    template_name = "login/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid(): 
            messages.error(request, "Failed to Login", extra_tags='Please complete the form properly')
            return render(request, self.template_name, {"form": form})
        
        user = form.cleaned_data['user']
        token = Auth(JWT()).encode(user)
        res = redirect('/')
        res.set_cookie(
            key = "token", 
            value = token,
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = False,
            httponly = True,
            samesite = False
        )
        messages.success(request, "Welcome "+ user.username, extra_tags='You have logged in successfully')
        return res


class Logout(ProtectedView):

    def post(self, request, *args, **kwargs):
        res = redirect('/signin')
        res.delete_cookie('token')
        res.delete_cookie('csrftoken')
        return res


class Profile(ProtectedView):
    template_name = 'profile/profile.html'
    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user = GeneralUserSerializer(user).data
        context['user'] = user
        return render(request, self.template_name, context)
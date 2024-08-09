from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from app.models import GeneralUser
from django.views import generic
from django.http import HttpRequest
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username or not password: return self.cleaned_data

        try:
            user = GeneralUser.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error('password', "Wrong password")
                raise forms.ValidationError("Wrong password")
        except GeneralUser.DoesNotExist as e:
            self.add_error('username', "Username "+ username +" does not exist")
            raise forms.ValidationError("Username "+ username +" does not exist")


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = GeneralUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


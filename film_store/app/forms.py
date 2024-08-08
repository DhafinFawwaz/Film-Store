from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from app.models import GeneralUser
from django.views import generic
from django.http import HttpRequest



class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = GeneralUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

def sign_up_form(request):

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('/')
        else:
            return render(request, 'register.html', {'form': form})

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

def sign_in_form(request: HttpRequest):

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})    
   
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have signed in successfully.')
            
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Error")
        else:
            messages.error(request, "Username or password incorrect")
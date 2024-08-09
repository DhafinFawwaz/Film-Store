from app.models import GeneralUser
from app.serializers import GeneralUserSerializer
from app.api.auth import register
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from .. import forms
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from app.views.views_class import PublicView, ProtectedView
from django.http import HttpResponseNotAllowed

class Register(PublicView):
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
        # messages.success(request, 'You have signed up successfully.')
        return redirect('/login')
        


class Login(PublicView):
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
                # messages.error(request, "Wrong password")
                return render(request, self.template_name, {"form": form})
            else:
                # messages.success(request, 'You have signed in successfully.')
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

class Logout(ProtectedView):

    def post(self, request, *args, **kwargs):
        res = redirect('/login')
        res.delete_cookie('token')
        res.delete_cookie('csrftoken')
        return res


class Profile(ProtectedView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user = GeneralUser.objects.get(id=user.id) # TODO: Handle exception
        user = GeneralUserSerializer(user).data
        context['user'] = user
        return render(request, self.template_name, context)
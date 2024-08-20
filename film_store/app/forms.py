from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django import forms
from app.models import GeneralUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'icon_src': 'https://api.iconify.design/mdi/user.svg?color=%2354565c', 'placeholder': 'Username/Email', 'class': 'text-night-50'}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'icon_src': 'https://api.iconify.design/mdi/password.svg?color=%2354565c', 'placeholder': 'Password'}))

    # modify label
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Username/Email"

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username or not password: return self.cleaned_data

        user = None

        try:
            validate_email(username)
            try: 
                user = GeneralUser.objects.get(email=username)
            except GeneralUser.DoesNotExist as e:
                self.add_error('username', username +" does not exist")
                raise forms.ValidationError(username +" does not exist")
        except forms.ValidationError as e:
            try: user = GeneralUser.objects.get(username=username)
            except GeneralUser.DoesNotExist as e:
                self.add_error('username', username +" does not exist")
                raise forms.ValidationError(username +" does not exist")
        
        
        if user.check_password(password):
            self.cleaned_data['user'] = user
            return self.cleaned_data
        else:
            self.add_error('password', "Wrong password")
            raise forms.ValidationError("Wrong password")


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'icon_src': 'https://api.iconify.design/mdi/user.svg?color=%2354565c', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'icon_src': 'https://api.iconify.design/mdi/user.svg?color=%2354565c', 'placeholder': 'Last Name'}))

    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'icon_src': 'https://api.iconify.design/mdi/email.svg?color=%2354565c', 'placeholder': 'email@email.com'}))
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'icon_src': 'https://api.iconify.design/mdi/user.svg?color=%2354565c', 'placeholder': 'Username'}))

    password1 = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'icon_src': 'https://api.iconify.design/mdi/password.svg?color=%2354565c', 'placeholder': 'SuperSecret123$$$'}), label="Password")
    password2 = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'icon_src': 'https://api.iconify.design/mdi/password.svg?color=%2354565c', 'placeholder': 'SuperSecret123$$$'}), label="Confirm Password")

    usable_password = None

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)



    class Meta:
        model = GeneralUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


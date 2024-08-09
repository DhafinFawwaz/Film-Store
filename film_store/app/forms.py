from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django import forms
from app.models import GeneralUser
from rest_framework_simplejwt.tokens import RefreshToken

class LoginForm(forms.Form):
    input_style = "bg-gray-50 border text-gray-900 sm:text-sm rounded-lg block w-full p-2.5 border-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-600 focus:border-blue-600 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': input_style}), label="Username", required=True)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'class': input_style}), label="Password", required=True)

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


from django.views.generic.base import TemplateView
 
class Login(TemplateView):
    template_name = 'login.html'

class Register(TemplateView):
    template_name = 'register.html'
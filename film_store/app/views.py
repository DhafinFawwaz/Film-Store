from django.views.generic.base import TemplateView
 
class Login(TemplateView):
    template_name = 'login.html'

class Register(TemplateView):
    template_name = 'register.html'

class Details(TemplateView):
    template_name = 'details.html'

class Bought(TemplateView):
    template_name = 'bought.html'

class Review(TemplateView):
    template_name = 'review.html'

class Profile(TemplateView):
    template_name = 'profile.html'

class Wishlist(TemplateView):
    template_name = 'wishlist.html'

class Browse(TemplateView):
    template_name = 'browse.html'
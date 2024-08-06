from django.views.generic.base import TemplateView
from app.models import GeneralUser, Film
from app.serializers import GeneralUserSerializer, FilmResponseSerializer
from django.http import HttpResponseRedirect
from django.urls import reverse

class ProtectedView(TemplateView):
    def get(self, request, *args, **kwargs):
        # if not self.request.user.is_authenticated:
        #     return HttpResponseRedirect('/login')
        return super().get(request, *args, **kwargs)

class PublicView(TemplateView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)
 
class Login(PublicView):
    template_name = 'login.html'

class Register(PublicView):
    template_name = 'register.html'

class Details(ProtectedView):
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film_id = kwargs['id']
        film = Film.objects.get(id=film_id)
        film = FilmResponseSerializer(film).data
        context['film'] = film
        return context

class Bought(ProtectedView):
    template_name = 'bought.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = GeneralUser.objects.all()[1]
        films = user.films.all()
        context['films'] = films
        return context

class Review(ProtectedView):
    template_name = 'review.html'

class Profile(ProtectedView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = GeneralUserSerializer(user).data
        context['user'] = user
        return context

class Wishlist(ProtectedView):
    template_name = 'wishlist.html'

class Browse(ProtectedView):
    template_name = 'browse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        films = Film.objects.all()
        films = FilmResponseSerializer(films, many=True).data
        context['films'] = films
        return context
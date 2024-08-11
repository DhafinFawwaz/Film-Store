from app.models import GeneralUser, Film, Review
from app.serializers import GeneralUserSerializer, FilmResponseSerializer, ReviewSerializer
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from .. import forms
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from app.views.views_class import PublicView, ProtectedView
from app.utils import duration_to_format, format_date_from_str

class Browse(ProtectedView):
    template_name = 'browse/browse.html'

    def get_recommendations(self, user):
        return Film.objects.all()[:5]

    

    def get(self, request, *args, **kwargs):
        context = {}
        if 'q' in self.request.GET:
            query = self.request.GET['q']
            films = Film.objects.filter(title__icontains=query)
            films = FilmResponseSerializer(films, many=True).data
            context['films'] = films
            context['query'] = query
            return render(request, self.template_name, context)

        films = Film.objects.all()
        films = FilmResponseSerializer(films, many=True).data
        for film in films:
            film['duration'] = duration_to_format(film['duration'])

        context['films'] = films
        return render(request, self.template_name, context)

class Details(ProtectedView):
    template_name = 'details/details.html'

    def get(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        user: GeneralUser = self.request.user

        # check if film is bought
        context['is_purchased'] = user.bought_films.filter(id=film.id).exists()

        # check if film is in wishlist
        context['in_wishlist'] = user.wishlist_films.filter(id=film.id).exists()

        # my review
        review = Review.objects.filter(film=film, user=user)
        if review.exists():
            review = review.first()
            review = ReviewSerializer(review).data
            review['created_at'] = format_date_from_str(review['created_at'])
            context['review'] = review

        # all reviews
        reviews = Review.objects.filter(film=film).exclude(review__isnull=True)
        reviews = ReviewSerializer(reviews, many=True).data
        for review in reviews:
            review['updated_at'] = format_date_from_str(review['updated_at'])
        context['all_review'] = reviews

        # Calculate average rating
        reviews = Review.objects.filter(film=film)
        if reviews.exists():
            rating = 0
            for review in reviews:
                rating += review.rating
            rating = rating / reviews.count()
            rating = round(rating, 2)
            context['avg_rating'] = rating
        else:
            context['avg_rating'] = 0
        

        film = FilmResponseSerializer(film).data
        film['duration'] = duration_to_format(film['duration'])
        context['film'] = film
        context['balance_left_if_purchased'] = request.user.balance - film['price']
        context['is_balance_sufficient'] = request.user.balance >= film['price']

        return render(request, self.template_name, context)
        
class BuyFilm(ProtectedView):
    def post(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        user: GeneralUser = self.request.user

        if user.balance < film.price:
            messages.error(request, 'Insufficient Balance', extra_tags="You don't have enough balance to purchase this film")
            return redirect(f'/details/{film_id}')
        
        user.bought_films.add(film)
        user.balance -= film.price

        # remove from wishlist if present
        if user.wishlist_films.filter(id=film.id).exists():
            user.wishlist_films.remove(film)
        
        user.save()

        messages.success(request, 'Film Purchased', extra_tags='Your purchase was successful, you can see it in your bought films|/bought', )
        return redirect(f'/details/{film_id}')
    
class WishlistFilm(ProtectedView):
    def post(self, request, *args, **kwargs):
        print(request.POST['_method'])
        if request.POST['_method'] == 'delete':
            return self.delete(request, *args, **kwargs)
        elif request.POST['_method'] == 'put':
            return self.put(request, *args, **kwargs)
        else:
            messages.error(request, 'Invalid Request', extra_tags='Invalid request method')
            return redirect('/')
    
    def put(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        user: GeneralUser = self.request.user

        if user.wishlist_films.filter(id=film.id).exists():
            messages.error(request, 'Film Already Wishlisted', extra_tags='The film you are already in your wishlist')
            return redirect(f'/details/{film_id}')
        
        user.wishlist_films.add(film)
        user.save()

        messages.success(request, 'Film Wishlisted', extra_tags='Your wishlist was successful, you can see it in your wishlist|/wishlist', )
        return redirect(f'/details/{film_id}')
    
    def delete(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        user: GeneralUser = self.request.user

        if not user.wishlist_films.filter(id=film.id).exists():
            messages.error(request, 'Film Not in Wishlist', extra_tags='The film is not in your wishlist')
            return redirect(f'/details/{film_id}')
        
        user.wishlist_films.remove(film)
        user.save()

        messages.success(request, 'Film Removed from Wishlist', extra_tags='The film was removed from your wishlist', )
        return redirect(f'/details/{film_id}')

class Bought(ProtectedView):
    template_name = 'bought/bought.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user: GeneralUser = self.request.user
        films = user.bought_films.all()
        films = FilmResponseSerializer(films, many=True).data
        for film in films:
            film['duration'] = duration_to_format(film['duration'])
        context['films'] = films
        return render(request, self.template_name, context)

class Wishlist(ProtectedView):
    template_name = 'wishlist/wishlist.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user: GeneralUser = self.request.user
        films = user.wishlist_films.all()
        films = FilmResponseSerializer(films, many=True).data
        context['films'] = films
        return render(request, self.template_name, context)

class ReviewView(ProtectedView):
    template_name = 'review/review.html'

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

class Rate(ProtectedView):
    def post(self, request, *args, **kwargs):
        context = {}
        rate = request.POST['rating']
        if rate not in ['1', '2', '3', '4', '5']:
            messages.error(request, 'Invalid Rating', extra_tags='Rating should be between 1 and 5')
            return redirect(f'/details/{kwargs["id"]}')
        
        film_id = kwargs['id']
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        
        user: GeneralUser = self.request.user
        review = Review.objects.filter(film=film, user=user)
        if review.exists():
            review = review.first()
            review.rating = rate
            messages.success(request, 'Rating Updated', extra_tags='Your rating was updated')
            review.save()
        else:
            review = Review.objects.create(film=film, user=user, rating=rate)
            messages.success(request, 'Rating Added', extra_tags='Your rating was added')
            review.save()

        return redirect(f'/details/{kwargs["id"]}')

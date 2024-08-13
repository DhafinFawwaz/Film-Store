from app.models import GeneralUser, Film, Review
from app.serializers import GeneralUserSerializer, FilmResponseSerializer, ReviewSerializer
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from .. import forms
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from app.views.views_class import UnauthorizedView, ProtectedView
from app.utils import duration_to_format, format_date_from_str, clamp
from django.core.paginator import Paginator
from django.db.models import Q, Count

class Browse(ProtectedView):
    template_name = 'browse/browse.html'
    max_genre = 4

    def get_recommendations(self, user: GeneralUser):
        # in bought, find the director with most films
        # find other films by that director. This is a

        # in wishlist, find the director with most films
        # find other films by that director and that film is not a. This is b

        # in bought, find the genre with most films
        # find other films by that genre and that film neither a not b. This is c

        # in wishlist, find the genre with most films
        # find other films by that genre and that film neither a not b not c. This is d

        # combine a, b, c, d

        # if the total is less than 4, then add random films to make it 4
        # ensure that the films are not already in a, b, c, d
        # also ensure that the films are not already bought by the user and not in the wishlist


        recommendations = []
        # a, bought - director
        a_director = user.bought_films.values('director').annotate(count=Count('director')).order_by('-count').first()
        if a_director:
            a_films = Film.objects.filter(director=a_director['director']).exclude(id__in=user.bought_films.all()).exclude(id__in=user.wishlist_films.all())
            recommendations.extend(a_films[:1])

        # b, wishlist - director
        b_director = user.wishlist_films.values('director').annotate(count=Count('director')).order_by('-count').first()
        if b_director:
            b_films = Film.objects.filter(director=b_director['director']).exclude(id__in=user.bought_films.all()).exclude(id__in=user.wishlist_films.all()).exclude(id__in=[film.id for film in recommendations])
            recommendations.extend(b_films[:1])

        # c, bought - genre
        c_genre = user.bought_films.values('genre__id', 'genre__name').annotate(count=Count('genre')).order_by('-count').first()
        if c_genre:
            c_films = Film.objects.filter(genre__id=c_genre['genre__id']).exclude(id__in=user.bought_films.all()).exclude(id__in=user.wishlist_films.all()).exclude(id__in=[film.id for film in recommendations])
            recommendations.extend(c_films[:1])

        # d, wishlist - genre
        d_genre = user.wishlist_films.values('genre__id', 'genre__name').annotate(count=Count('genre')).order_by('-count').first()
        if d_genre:
            d_films = Film.objects.filter(genre__id=d_genre['genre__id']).exclude(id__in=user.bought_films.all()).exclude(id__in=user.wishlist_films.all()).exclude(id__in=[film.id for film in recommendations])
            recommendations.extend(d_films[:1])

        # combine
        if len(recommendations) < 4:
            additional_films = Film.objects.exclude(id__in=user.bought_films.all()).exclude(id__in=user.wishlist_films.all()).exclude(id__in=[film.id for film in recommendations]).order_by('?')
            slice_len = 4 - len(recommendations)
            recommendations.extend(additional_films[:slice_len])

        return recommendations


    def get(self, request, *args, **kwargs):
        context = {}
        films = []
        if 'q' in self.request.GET and self.request.GET['q'] != '':
            query = self.request.GET['q']
            films = Film.objects.filter(
                Q(title__icontains=query) | Q(director__icontains=query)
            ).order_by('-release_year')
            context['query'] = query
        else:
            films = Film.objects.all().order_by('-release_year')

        if 'q' not in self.request.GET :
            page = self.request.GET.get('page')
            if not page or page == '1':
                recommendations = self.get_recommendations(self.request.user)
                recommendations = FilmResponseSerializer(recommendations, many=True).data
                for film in recommendations:
                    film['duration'] = duration_to_format(film['duration'])
                    if len(film['genre']) > self.max_genre:
                        film['genre'] = film['genre'][:self.max_genre]
                        film['genre'].append('...')
                context['recommendations'] = recommendations

        paginator = Paginator(films, 8)
        page = 1
        if 'page' in self.request.GET:
            page = int(self.request.GET['page'])
            page = clamp(page, 1, paginator.num_pages)
        films = paginator.get_page(page)
        elided_page = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)

        context['elided_page'] = elided_page
        context['prev_page'] = page - 1 if page > 1 else None
        context['next_page'] = page + 1 if page < paginator.num_pages else None
        context['current_page'] = page


        films = FilmResponseSerializer(films, many=True).data
        for film in films:
            film['duration'] = duration_to_format(film['duration'])
            if len(film['genre']) > self.max_genre:
                film['genre'] = film['genre'][:self.max_genre]
                film['genre'].append('...')

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

        context['is_purchased'] = user.bought_films.filter(id=film.id).exists()
        context['in_wishlist'] = user.wishlist_films.filter(id=film.id).exists()

        # my review
        review = Review.objects.filter(film=film, user=user)
        if review.exists():
            review = review.first()
            review = ReviewSerializer(review).data
            review['created_at'] = format_date_from_str(review['created_at'])
            context['review'] = review

        # all reviews
        reviews = Review.objects.filter(film=film).exclude(review__isnull=True).order_by('-updated_at')[:3]
        reviews = ReviewSerializer(reviews, many=True).data
        for review in reviews:
            review['updated_at'] = format_date_from_str(review['updated_at'])
        context['all_review'] = reviews

        # Calculate average rating
        reviews = Review.objects.filter(film=film)
        if reviews.exists():
            rating = 0
            for review in reviews:
                rating += review.rating if review.rating else 0
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
    max_genre = 4

    def get(self, request, *args, **kwargs):
        context = {}
        user: GeneralUser = self.request.user
        films = user.bought_films.all().order_by('-release_year')
        films = FilmResponseSerializer(films, many=True).data


        paginator = Paginator(films, 8)
        page = 1
        if 'page' in self.request.GET:
            page = int(self.request.GET['page'])
            page = clamp(page, 1, paginator.num_pages)
        films = paginator.get_page(page)
        elided_page = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)

        context['elided_page'] = elided_page
        context['prev_page'] = page - 1 if page > 1 else None
        context['next_page'] = page + 1 if page < paginator.num_pages else None
        context['current_page'] = page


        for film in films:
            film['duration'] = duration_to_format(film['duration'])
            if len(film['genre']) > self.max_genre:
                film['genre'] = film['genre'][:self.max_genre]
                film['genre'].append('...')
        context['films'] = films
        return render(request, self.template_name, context)

class Wishlist(ProtectedView):
    template_name = 'wishlist/wishlist.html'
    max_genre = 4

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        user: GeneralUser = self.request.user
        films = user.wishlist_films.all().order_by('-release_year')
        films = FilmResponseSerializer(films, many=True).data


        paginator = Paginator(films, 8)
        page = 1
        if 'page' in self.request.GET:
            page = int(self.request.GET['page'])
            page = clamp(page, 1, paginator.num_pages)
        films = paginator.get_page(page)
        elided_page = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)

        context['elided_page'] = elided_page
        context['prev_page'] = page - 1 if page > 1 else None
        context['next_page'] = page + 1 if page < paginator.num_pages else None
        context['current_page'] = page


        for film in films:
            film['duration'] = duration_to_format(film['duration'])
            if len(film['genre']) > self.max_genre:
                film['genre'] = film['genre'][:self.max_genre]
                film['genre'].append('...')
        context['films'] = films
        return render(request, self.template_name, context)

class ReviewView(ProtectedView):
    template_name = 'review/review.html'

    def get(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        
        context['film'] = FilmResponseSerializer(film).data

        reviews = Review.objects.filter(film=film).exclude(review__isnull=True).order_by('-updated_at')
        paginator = Paginator(reviews, 4)
        page = 1
        if 'page' in self.request.GET:
            page = int(self.request.GET['page'])
            page = clamp(page, 1, paginator.num_pages)
        reviews = paginator.get_page(page)
        elided_page = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)

        context['elided_page'] = elided_page
        context['prev_page'] = page - 1 if page > 1 else None
        context['next_page'] = page + 1 if page < paginator.num_pages else None
        context['current_page'] = page

        reviews = ReviewSerializer(reviews, many=True).data
        for review in reviews:
            review['updated_at'] = format_date_from_str(review['updated_at'])
        context['all_review'] = reviews

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        review_text = request.POST['review']
        if not review_text or review_text == '': 
            messages.error(request, 'Invalid Review', extra_tags='Review should not be empty')
            return redirect(f'/details/{film_id}')

        
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        
        user: GeneralUser = self.request.user
        review = Review.objects.filter(film=film, user=user)
        if review.exists():
            review = review.first()
            if review.review: messages.success(request, 'Review Updated', extra_tags='Your review was updated')
            else: messages.success(request, 'Review Added', extra_tags='Your review was added')
            review.review = review_text
            review.save()
        else:
            review = Review.objects.create(film=film, user=user, review=review_text)
            messages.success(request, 'Review Added', extra_tags='Your review was added')
            review.save()

        return redirect(f'/details/{film_id}')

class Rate(ProtectedView):
    def post(self, request, *args, **kwargs):
        context = {}
        film_id = kwargs['id']
        rate = request.POST['rating']
        if rate not in ['1', '2', '3', '4', '5']:
            messages.error(request, 'Invalid Rating', extra_tags='Rating should be between 1 and 5')
            return redirect(f'/details/{film_id}')
        
        film: Film = None
        try: film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            messages.error(request, 'Film not found', extra_tags='The film you are looking for does not exist')
            return redirect('/')
        
        user: GeneralUser = self.request.user
        review = Review.objects.filter(film=film, user=user)
        if review.exists():
            review = review.first()
            if review.rating: messages.success(request, 'Rating Updated', extra_tags='Your rating was updated')
            else: messages.success(request, 'Rating Added', extra_tags='Your rating was added')
            review.rating = rate
            review.save()
        else:
            review = Review.objects.create(film=film, user=user, rating=rate)
            messages.success(request, 'Rating Added', extra_tags='Your rating was added')
            review.save()

        return redirect(f'/details/{kwargs["id"]}')

class Watch(ProtectedView):
    template_name = 'watch/watch.html'

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
        if user.bought_films.filter(id=film.id).exists():
            context['is_purchased'] = True
        else:
            messages.error(request, 'Film not Purchased', extra_tags='You need to purchase the film to watch it')
            return redirect(f'/details/{film_id}')
        film = FilmResponseSerializer(film).data
        context['film'] = film
        return render(request, self.template_name, context)
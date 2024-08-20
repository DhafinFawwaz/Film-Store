import requests
import zipfile
from tqdm import tqdm
import json
import os
from django.conf import settings
from app.models import Film, Genre, GeneralUser, Review
from app.serializers import GenreSerializer, GeneralUserSerializer, ReviewSerializer
from datetime import datetime
from django.core.files import File
from django.db.models import signals
from app.signals import film_signals, user_signals, review_signals

def download_dataset():
    if os.path.exists("dataset"): return

    url = settings.DATASET_URL

    print("Downloading dataset.zip...")

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open("dataset.zip", "wb") as file:
        for data in tqdm(response.iter_content(chunk_size=1024), total=total_size//1024, unit='KB'):
            file.write(data)

    print("Extracting dataset.zip...")
    with zipfile.ZipFile("dataset.zip", 'r') as zip_ref:
        zip_ref.extractall("dataset")

    print("Done")

def clear_db():
    Genre.objects.all().delete()
    Film.objects.all().delete()
    GeneralUser.objects.exclude(is_superuser=True).delete()
    Review.objects.all().delete()

def disable_signals():
    signals.post_save.disconnect(receiver=film_signals.invalidate_film_cache, sender=Film)
    signals.post_delete.disconnect(receiver=film_signals.invalidate_film_cache_on_delete, sender=Film)
    signals.post_save.disconnect(receiver=review_signals.invalidate_review_cache, sender=Review)
    signals.post_delete.disconnect(receiver=review_signals.invalidate_review_cache_on_delete, sender=Review)
    signals.m2m_changed.disconnect(receiver=user_signals.invalidate_user_cache_on_bought_film_change, sender=GeneralUser.bought_films.through)
    signals.m2m_changed.disconnect(receiver=user_signals.invalidate_user_cache_on_bought_film_change, sender=GeneralUser.wishlist_films.through)


def enable_signals():
    signals.post_save.connect(receiver=film_signals.invalidate_film_cache, sender=Film)
    signals.post_delete.connect(receiver=film_signals.invalidate_film_cache_on_delete, sender=Film)
    signals.post_save.connect(receiver=review_signals.invalidate_review_cache, sender=Review)
    signals.post_delete.connect(receiver=review_signals.invalidate_review_cache_on_delete, sender=Review)
    signals.m2m_changed.connect(receiver=user_signals.invalidate_user_cache_on_bought_film_change, sender=GeneralUser.bought_films.through)
    signals.m2m_changed.connect(receiver=user_signals.invalidate_user_cache_on_bought_film_change, sender=GeneralUser.wishlist_films.through)

def start_seeding():
    dataset = json.load(open("dataset/dataset.json"))

    print("Seeding genres...")
    for genre in dataset["genre"]:
        g = Genre.objects.create(name=genre)
        g.save()

    print("Seeding films...")
    for film in dataset["films"]:
        title = film['name']
        description = film['description']
        director = film['director']
        release_year = film['datePublished']
        release_year = datetime.strptime(release_year, "%Y-%m-%d")
        release_year  = release_year.year; release_year = int(release_year) if release_year else None

        genre_list = film['genre']
        price = film['price']; price = int(price) if price else None
        duration = film['duration']; duration = int(duration) if duration else None
        video = open(film['video'], 'rb')
        cover_image = open(film['image'], 'rb')
        
        with open(film['video'], 'rb') as video_file, open(film['image'], 'rb') as image_file:
            video = File(video_file)
            cover_image = File(image_file)
            
            f = Film.objects.create(
                title=title,
                description=description,
                director=director,
                release_year=release_year,
                price=price,
                duration=duration,
                video=video,
                cover_image=cover_image
            )

            for genre in genre_list:
                g = Genre.objects.get(name=genre)
                f.genre.add(g)

    print("Seeding users...")
    for user in dataset["user"]:
        username = user['username']
        email = user['email']
        password = "bebek123"
        first_name = user['first_name']
        last_name = user['last_name']
        bought = user['bought']
        wishlist = user['wishlist']
        balance = user['balance']; balance = int(balance) if balance else None

        u = GeneralUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            balance=balance
        )
        u.save()

        for b in bought:
            f = Film.objects.get(title=b)
            u.bought_films.add(f)
        
        for w in wishlist:
            f = Film.objects.get(title=w)
            u.wishlist_films.add(f)

        u.save()


    print("Seeding reviews...")
    for rev in dataset["review"]:
        film = rev['film']
        user = rev['username']
        text = rev['review']
        rating = rev['rating']; rating = int(rating) if rating else None
        created_at = rev['created_at']
        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

        r = Review.objects.create(
            film=Film.objects.get(title=film),
            user=GeneralUser.objects.get(username=user),
            review=text,
            rating=rating,
            created_at=created_at
        )
        r.save()


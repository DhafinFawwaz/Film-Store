from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import GeneralUser, Genre, Film, Review
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
import re
from app.utils import duration_to_format
from app.utils import format_date_from_str

class PasswordValidator:
    def __call__(self, value):
        if len(value) < 8:
            raise ValidationError(f"Password must be at least 8 characters long")
        if len(value) >= 255:
            raise ValidationError(f"Password must be less than 256 characters long")
        if not any(char.isdigit() for char in value):
            raise ValidationError(f"Password must contain at least one digit")
        if not any(char.isupper() for char in value):
            raise ValidationError(f"Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValidationError(f"Password must contain at least one lowercase letter")
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in value):
            raise ValidationError(f"Password must contain at least one special character")

class GeneralUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    username = serializers.CharField(required=True, min_length=4, max_length=30, validators=[UniqueValidator(queryset=GeneralUser.objects.all(), message="This username is taken")])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=GeneralUser.objects.all(), message="This email is taken")])
    password = serializers.CharField(required=True, validators=[PasswordValidator()], write_only=True)
    first_name = serializers.CharField(required=True, min_length=1, max_length=30)
    last_name = serializers.CharField(required=True, min_length=1, max_length=30)
    balance = serializers.DecimalField(required=True, max_digits=12, decimal_places=2)
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    class Meta:
        model = GeneralUser
        fields = [
            "id",
            "username",
            "email",
            "password",
            "balance",
            "first_name",
            "last_name"
        ]

class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Genre
        fields = ["name"]

def is_duration_format_valid(duration: str):
    return re.match(r"\d\d:[0-5]\d:[0-5]\d", duration)

class DurationValidator:
    def __call__(self, value):
        # hh:mm:ss
        if not is_duration_format_valid(value):
            raise ValidationError(f"Duration must be in the format hh:mm:ss")

class FilmRequestSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    director = serializers.CharField(required=True)
    release_year = serializers.IntegerField(required=True)
    genre = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    duration = serializers.IntegerField(required=True)
    video = serializers.FileField(required=True)
    cover_image = serializers.ImageField(required=False)

    class Meta:
        model = Film
        fields = ["title", "description", "director", "release_year", "genre", "price", "duration", "video", "cover_image"]

class FilmResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    director = serializers.CharField(required=True)
    release_year = serializers.IntegerField(required=True)
    genre = GenreSerializer(required=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    duration = serializers.IntegerField(required=True)
    video = serializers.URLField(allow_blank=True)
    cover_image = serializers.URLField(allow_blank=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = Film
        fields = ["id", "title", "description", "director", "release_year", "genre", "price", "duration", "video", "cover_image", "created_at", "updated_at"]

    def to_representation(self, val):
        representation = super().to_representation(val)
        representation['video_url'] = val.video.url
        representation['cover_image_url'] = val.cover_image.url
        genre_list = val.genre.all()
        representation['genre'] = [genre.name for genre in genre_list]
        representation.pop('video')
        representation.pop('cover_image')
        return representation
    
class FilmViewContextSerializer(FilmResponseSerializer):
    def to_representation(self, val):
        representation = super().to_representation(val)

        max_genre = 4
        representation['duration'] = duration_to_format(representation['duration'])
        
        arr = []
        genre_list = val.genre.all()
        for genre in genre_list:
            if len(arr) >= max_genre: 
                arr.append("...")
                break
            arr.append(genre.name)
        representation['genre'] = arr

        return representation

class ReviewSerializer(serializers.Serializer):
    user = GeneralUserSerializer(required=True)
    rating = serializers.IntegerField(required=True)
    review = serializers.CharField(required=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = Review
        fields = ["rating", "review", "created_at", "updated_at", "user"]

class ReviewViewContextSerializer(ReviewSerializer):
    def to_representation(self, val):
        representation = super().to_representation(val)
        representation['updated_at'] = format_date_from_str(representation['updated_at'])
        return representation
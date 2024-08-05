from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import GeneralUser, Genre, Film
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

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
    username = serializers.CharField(required=True, min_length=4, max_length=30, validators=[UniqueValidator(queryset=GeneralUser.objects.all(), message="Username is taken")])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=GeneralUser.objects.all(), message="Email is taken")])
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

class FilmSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    title = serializers.CharField(max_length=255)
    director = serializers.CharField(max_length=255)

    release_year = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    duration = serializers.IntegerField()
    video_url = serializers.URLField()
    cover_image_url = serializers.URLField()

    class Meta:
        model = Film
        fields = ["title", "description", "director", "release_year", "genre", "price", "duration", "video_url", "cover_image_url"]

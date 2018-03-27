from rest_framework import serializers

from .models import *


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewProfile
        fields = ['id', 'name', 'age', 'description', 'gender', 'link', 'role']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["genre"]


class MovieSerializer(serializers.ModelSerializer):
    casts = CrewSerializer(many=True, read_only=True)
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "synopsis", "language", "casts", "genres"]


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ["id", "name", "location_lat", "location_long"]


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ["id", "movie", "screen", "time"]

from django.core.management.base import BaseCommand
import django.core.exceptions as exceptions
import django.db as db
import booking_system.models as M
from datetime import datetime
import pandas as pd
import funcy as fy
import random 
import numpy
from . import mldt

from ast import literal_eval
from pprint import pprint

gender_map = dict([
    (0, "Male"),
    (1, "Female"),
    (2, "Male")
])


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            help='File path',
        )

    def handle(self, *args, **options):
        self.seed(options['path'])


    def seed(self, path):
        data = mldt.load(path)
        self.prototype(data)

    def mapping(self, _m, df):
        _d = {}
        for key in _m:
            _d[key] = df[_m[key]]
        return _d

    def _movie(self, mf): 
        _mapping = {
           "synopsis": "overview", 
           "tagline": "tagline" ,
           "title": "title",
           "release_date": "release_date",
           "imdb_id": "imdb_id",
        }


        params = self.mapping(_mapping, mf)
        try:
            movie = M.Movie.objects.get(imdb_id=params["imdb_id"])

        except exceptions.ObjectDoesNotExist:
            lang = self._language(mf["original_language"])
            movie = M.Movie.objects.create(**params, language=lang)

            movie.save()
            self._aggregate_rating(movie, mf)
            self._genres(movie, mf)

        return movie

    def _aggregate_rating(self, movie, mf):
        _mapping = {
                "average": "vote_average",
                "count": "vote_count",
                "popularity": "popularity"
        }
        params = self.mapping(_mapping, mf)
        rating = M.AggregateRating.objects.create(movie=movie,
                **params)
        rating.save()
    
    def _genres(self, movie, mf):
        serialized_genre = mf["genres"]
        genres = literal_eval(serialized_genre)
        _genres = []
        for genre in genres:
            _genre = self._genre(genre["name"])
            _genres.append(_genre)
        movie.genres.set(_genres)

    def _genre(self, genre):
        _genre = None
        try:
            _genre = M.Genre.objects.get(genre=genre)
        except exceptions.ObjectDoesNotExist:
            _genre = M.Genre.objects.create(genre=genre)
            _genre.save()
        return _genre

    def _cast(self, cf):
        pass

    def _language(self, lang):
        try:
            _lang = M.Language.objects.get(lang=lang)
        except exceptions.ObjectDoesNotExist:
            _lang = M.Language.objects.create(lang=lang)
            _lang.save()
        return _lang

    def _gender(self, name):
        try:
            _gender = M.Gender.objects.get(name=name)
        except exceptions.ObjectDoesNotExist:
            _gender = M.Gender.objects.create(name=name)
            _gender.save()
        return _gender


    def _crew_profile(self, profile):
        try:
            _profile = M.CrewProfile.objects.get(name=profile["name"])
        except exceptions.ObjectDoesNotExist:
            _id = profile["gender"]
            _gender = self._gender(gender_map[_id])
            print(profile["name"], gender_map[_id])
            _profile = M.CrewProfile.objects.create(name=profile["name"],
                    gender=_gender)
            _profile.save()
        return _profile

    def _add_movie_crew(self, crew, movie_id):
        try:
            movie = M.Movie.objects.get(pk=movie_id)
            movie.crew.add(crew)
            movie.save()
        except exceptions.ObjectDoesNotExist:
            print("Deferring movie!")


    def _casts(self, cast, movie_id):
        cast = literal_eval(cast)
        cast_type = self._cast_type("Actor")
        for profile in cast:
            _profile = self._crew_profile(profile)
            _crew = self._crew(_profile, cast_type)
            self._add_movie_crew(_crew, movie_id)


    def _cast_type(self, name):
        try:
            _cast_type = M.CastType.objects.get(name=name)
        except exceptions.ObjectDoesNotExist:
            _cast_type = M.CastType.objects.create(name=name)
            _cast_type.save()
        return _cast_type

    def _crew(self, _profile, cast_type):
        try:
            _crew = M.Crew.objects.get(profile=_profile, role=cast_type)
        except exceptions.ObjectDoesNotExist:
            _crew = M.Crew.objects.create(profile=_profile, role=cast_type)
            _crew.save()
        return _crew


    def prototype(self, data):

        movies = data["movies_metadata"]
        for i, movie in movies.iterrows():
            self._movie(movie)

        credits = data["credits"]
        for i, x in credits.iterrows():
            cast, crew, _id = x
            self._casts(cast, _id)
            director = mldt.director(literal_eval(crew))
            if director is not None:
                _profile = self._crew_profile(director)
                cast_type = self._cast_type("Director")
                _crew = self._crew(_profile, cast_type)
                self._add_movie_crew(crew, _id)



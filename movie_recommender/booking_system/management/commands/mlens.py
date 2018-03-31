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
        except ObjectDoesNotExist:
            _lang = M.Language.objects.create(lang=lang)
            _lang.save()
        return _lang

    def prototype(self, data):
        credits = data["credits"]
        #for i, x in credits.iterrows():
        #    cast, crew, _id = x
        #    mldt.cast(cast)
            #pprint(literal_eval(crew))
        M.Movie.objects.all().delete()

        movies = data["movies_metadata"]
        for i, movie in movies.iterrows():
            self._movie(movie)
            print(movie["title"])

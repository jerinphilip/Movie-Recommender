from django.core.management.base import BaseCommand
import booking_system.models as M
from datetime import datetime
import pandas as pd
import funcy as fy
import random 
import numpy


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            help='File path',
        )

    def handle(self, *args, **options):
        self.seed(options['path'])

    def _seed_languages(self, langs):
        M.Language.objects.all().delete()
        langs = set(list(langs))
        for lang in langs:
            _lang = M.Language.objects.create(lang=lang)
            _lang.save()

    def _seed_genres(self, genres):
        M.Genre.objects.all().delete()
        transform = lambda x: x.split('|')
        genres = list(map(transform, genres))
        genres = fy.flatten(genres)
        genres = set(genres)
        for genre in genres:
            _genre = M.Genre.objects.create(genre=genre)
            _genre.save()

    def _seed_movies(self, movies):
        M.Movie.objects.all().delete()
        for i, m in movies.iterrows():
            genres, title, link, lang, year = list(m.values)
            genres = genres.split('|')
            _lang = M.Language.objects.get(lang=lang)
            _movie = M.Movie.objects.create(title=title,
                    language=_lang)
            _genres = [M.Genre.objects.get(genre=g) for g in genres]
            _movie.genres.set(_genres)
            _movie.save()

    def _seed_cast(self, cast):
        M.Cast.objects.all().delete()
        directors = set()
        actors = set()
        for i, c in cast.iterrows():
            directors.add(c[0])
            actors.add(c[1])
            actors.add(c[2])
            actors.add(c[3])
        for director in directors:
            _cast = M.Cast.objects.create(name=director, cast_type=2, gender=1)
            _cast.save()
        for actor in actors:
            _cast = M.Cast.objects.create(name=actor, cast_type=1, gender=1)
            _cast.save()

    def _seed_seat_type(self):
        M.SeatType.objects.all().delete()
        s = [('Regular', 200),('Executive', 300)]
        for i in range(2): #Creating two seat types
            name = s[i][0]
            price = s[i][1]
            _seat_type = M.SeatType.objects.create(name=name, price=price)
            _seat_type.save()

    def _seed_theater(self):
        M.Theater.objects.all().delete()
        theaters = ["gold_plaza","silver_plaza","platinum_plaza"]
        latitude, longitude=0,0
        _seat_types = list(M.SeatType.objects.all())
        for theater in theaters:
            _theater = M.Theater.objects.create(name=theater,location_lat=latitude,
                                        location_long=longitude)
            _theater.save()
            for _seat_type in _seat_types:
                _theater.seat_types.add(_seat_type)

    def _seed_screens(self):
        M.Screen.objects.all().delete()
        _theaters=list(M.Theater.objects.all())
        _identifiers=['A','B','C','D']
        for _identifier in _identifiers:
            for _theater in _theaters:
                _screen=M.Screen.objects.create(identifier=_identifier, theater=_theater)
                _screen.save()

    def _seed_shows(self):
        M.Show.objects.all().delete()
        _screens = list(M.Screen.objects.all())
        _movies = list(M.Movie.objects.all())
        times = ['10:00:00', '2:00:00', '8:00:00']
        for _screen in _screens:
            for _time in times:
                for _movie in _movies:
                    time = datetime.strptime(_time, '%H:%M:%S').time()
                    _show = M.Show.objects.create(movie=_movie,screen=_screen,
                                                  time=time)
                    _show.save()

    def seed(self, path):
        df = pd.read_csv(path)
        df = df.head()
        self._seed_genres(df["genres"])
        self._seed_languages(df["language"])
        cast_params = [1, 6, 10, 14]
        cs = df.iloc[:, cast_params]
        self._seed_cast(cs)
        movie_params = [9, 11, 17, 19, 23]
        ms = df.iloc[:, movie_params]
        self._seed_movies(ms)
        self._seed_seat_type()
        self._seed_theater()
        self._seed_screens()
        self._seed_shows()

# 0 color
# 1 director_name
# 2 num_critic_for_reviews
# 3 duration
# 4 director_facebook_likes
# 5 actor_3_facebook_likes
# 6 actor_2_name
# 7 actor_1_facebook_likes
# 8 gross
# 9 genres
# 10 actor_1_name
# 11 movie_title
# 12 num_voted_users
# 13 cast_total_facebook_likes
# 14 actor_3_name
# 15 facenumber_in_poster
# 16 plot_keywords
# 17 movie_imdb_link
# 18 num_user_for_reviews
# 19 language
# 20 country
# 21 content_rating
# 22 budget
# 23 title_year
# 24 actor_2_facebook_likes
# 25 imdb_score
# 26 aspect_ratio
# 27 movie_facebook_likes


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

    def _seed_cast_type(self):
        M.CastType.objects.all().delete()
        c = ["Director", "Actor", "Producer"] #Creating three cast types
        for i in range(3):
            name = c[i]
            _cast_type = M.CastType.objects.create(name=name)
            _cast_type.save()

    def _seed_gender(self):
        M.Gender.objects.all().delete()
        g = ["Male", "Female"] #Creating two gender
        for i in range(2):
            name = g[i]
            _gender = M.Gender.objects.create(name=name)
            _gender.save()

    def _seed_languages(self, langs):
        M.Language.objects.all().delete()
        langs = set(list(langs))
        for lang in langs:
            _lang = M.Language.objects.create(lang=lang)
            _lang.save()

    def _seed_status_type(self):
        M.StatusType.objects.all().delete()
        s = ["Success", "Failure", "In Progress"] #Creating three cast types
        for i in range(3):
            name = s[i]
            _status_type = M.StatusType.objects.create(name=name)
            _status_type.save()

    def _seed_crew_profile(self, crew_profile):
        M.CrewProfile.objects.all().delete()
        _crew=set()
        for i, c in crew_profile.iterrows():
            _crew.add(c[0])
            _crew.add(c[1])
            _crew.add(c[2])
            _crew.add(c[3])
        g = "Male"
        for cp in _crew:
            _gender = M.Gender.objects.get(name=g)
            _crew_profile = M.CrewProfile.objects.create(name=cp,gender=_gender)
            _crew_profile.save()

    def _seed_genres(self, genres):
        M.Genre.objects.all().delete()
        transform = lambda x: x.split('|')
        genres = list(map(transform, genres))
        genres = fy.flatten(genres)
        genres = set(genres)
        for genre in genres:
            _genre = M.Genre.objects.create(genre=genre)
            _genre.save()

    def _seed_user_profile(self):
        M.UserProfile.objects.all().delete()
        M.User.objects.all().delete()
        _age = 23
        phones = ["0123456789", "1234567890", "2345678901"]#, "3456789012", "4567890123"]
        usernames = ['Harshil', 'Jerin', 'Mandar']
        passwords = ['Harshil', 'Jerin', 'Mandar']
        gen = "Male"
        genre_pref = ["Sci-Fi", "Fantasy"]
        _genre_pref = [M.Genre.objects.get(genre=g) for g in genre_pref]
        _gender = M.Gender.objects.get(name=gen)
        #creating 3 users
        for i in range(3):
            _user = M.User.objects.create(username=usernames[i], password=passwords[i], email="")
            _user.save()
            _user_profile = M.UserProfile.objects.create(gender=_gender, age=_age, phone=phones[i], user=_user)
            _user_profile.genre_pref.set(_genre_pref)
            _user_profile.save()

    def _seed_crew(self, crew):
        M.Crew.objects.all().delete()
        directors = set()
        actors = set()
        for i, c in crew.iterrows():
            directors.add(c[0])
            actors.add(c[1])
            actors.add(c[2])
            actors.add(c[3])
        d = "Director"
        a = "Actor"
        for director in directors:
            _profile = M.CrewProfile.objects.get(name=director)
            _role = M.CastType.objects.get(name=d)
            _crew = M.Crew.objects.create(profile=_profile, role=_role)
            _crew.save()
        for actor in actors:
            _profile = M.CrewProfile.objects.get(name=actor)
            _role = M.CastType.objects.get(name=a)
            _crew = M.Crew.objects.create(profile=_profile, role=_role)
            _crew.save()

    def _seed_movies(self, movies):
        M.Movie.objects.all().delete()
        for i, m in movies.iterrows():
            title, lang, genres, crew1, crew2, crew3, crew4 = list(m.values)
            genres = genres.split('|')
            _lang = M.Language.objects.get(lang=lang)
            _movie = M.Movie.objects.create(title=title,
                    language=_lang)
            #TODO roles of crew
            crew = [crew1, crew2, crew3, crew4]
            _crew = M.Crew.objects.filter(profile__name__in=crew)
            _movie.crew.set(_crew)
            _genres = [M.Genre.objects.get(genre=g) for g in genres]
            _movie.genres.set(_genres)
            _movie.save()

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

    def _seed_seat(self):
        M.Seat.objects.all().delete()
        _seat_type = M.SeatType.objects.all()[0]
        _screens = list(M.Screen.objects.all())
        _rows = map(chr, range(ord('A'), ord('Z')+1)) # rows from A - Z
        _columns = list(range(1,11)) # columns from 1 - 10
        for _screen in _screens:
            for _row in _rows:
                for _column in _columns:
                    _seat = M.Seat.objects.create(screen=_screen,row_id=_row,
                                                  col_id=_column,
                                                  seat_type=_seat_type)
                    _seat.save()

    def _seed_booking(self):
        M.Booking.objects.all().delete()
        phones = ["0123456789","1234567890", "2345678901"]#, "3456789012", "4567890123"]
        for p in phones:
            _user = M.UserProfile.objects.get(phone=p)
            _seats = M.Seat.objects.get(row_id='A', col_id=3)
            _type = M.SeatType.objects.get(name="Regular")
            _show = M.Show.objects.get(time='10:00:00')
            _booking = M.Booking.objects.create(user=_user, seats=_seats, show=_show, type=_type)
            _booking.save()

    def seed(self, path):
        df = pd.read_csv(path)
        # df = df.head(50)
        df = df.head(5)
        self._seed_cast_type()
        self._seed_gender()
        self._seed_languages(df["language"])
        self._seed_status_type()
        crew_profile_params=[1,10,6,14]
        cpp = df.iloc[:, crew_profile_params]
        self._seed_crew_profile(cpp)
        self._seed_genres(df["genres"])
        self._seed_user_profile()
        crew_params=[1,10,6,14]
        cp = df.iloc[:, crew_params]
        self._seed_crew(cp)
        movie_params = [11, 19, 9, 1, 10, 6, 14]
        ms = df.iloc[:, movie_params]
        self._seed_movies(ms)
        self._seed_seat_type()
        self._seed_theater()
        self._seed_screens()
        self._seed_shows()
        self._seed_seat()
        # self._seed_booking()
        # self._seed_invoice()
        # self._seed_review(s)

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

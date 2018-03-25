from django.core.management.base import BaseCommand
import booking_system.models as M
import pandas as pd
import funcy as fy


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

    def _seed_cast(self, params):
        pass

    def seed(self, path):
        df = pd.read_csv(path)
        df = df.head()
        self._seed_genres(df["genres"])
        self._seed_languages(df["language"])
        movie_params = [9, 11, 17, 19, 23]
        ms = df.iloc[:, movie_params]
        self._seed_movies(ms)

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


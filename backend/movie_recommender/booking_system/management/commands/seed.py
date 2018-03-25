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
        pass

    def seed(self, path):
        df = pd.read_csv(path)
        self._seed_genres(df["genres"])
        print(df.head())


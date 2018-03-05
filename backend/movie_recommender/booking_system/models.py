from django.db import models

# Create your models here.

CAST_TYPE = [(1, "actor"), (2, "director"), (3, "producer")]
GENDERS = [(1, "male"), (2, "female"), (3, "other")]
LANGUAGES = [(0, "english"), (1, "hindi"), (2, 'telugu')]


class Cast(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    age = models.IntegerField(default=0)
    gender = models.IntegerField(choices=GENDERS)
    link = models.TextField(default="")
    description = models.TextField(default="")
    cast_type = models.IntegerField(choices=CAST_TYPE)

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre


class Movie(models.Model):
    title = models.CharField(max_length=100, default="")
    synopsis = models.TextField(default="")
    language = models.IntegerField(choices=LANGUAGES)
    casts = models.ManyToManyField(Cast)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class SeatType(models.Model):
    name = models.CharField(max_length=100, default="")
    price = models.FloatField(default=0)


class Theater(models.Model):
    name = models.CharField(max_length=100, default="")
    location_lat = models.FloatField(default=0)
    location_long = models.FloatField(default=0)
    seat_types = models.ManyToManyField(SeatType)


class Screen(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10, default="")


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    time = models.TimeField()

from django.db import models

# Create your models here.

CAST_TYPE = [(1, "actor"), (2, "director"), (3, "producer")]
GENDERS = [(1, "male"), (2, "female"), (3, "other")]


class Cast(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    age = models.IntegerField(default=0)
    gender = models.CharField(choices=GENDERS, max_length=100)
    link = models.TextField(default="")
    description = models.TextField(default="")
    cast_type = models.CharField(max_length=100, choices=CAST_TYPE)

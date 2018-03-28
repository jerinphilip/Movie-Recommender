from django.contrib.auth.models import User
from booking_system.models import Movie
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Movie
        #'username': ['exact', 'contains'],
        fields = {'title': ['contains'],}
from rest_framework import generics
from .serializers import CastSerializer, Cast, MovieSerializer, Movie

# Create your views here.


class CastList(generics.ListCreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class CastDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


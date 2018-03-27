from rest_framework import generics
from .serializers import CastSerializer, Cast, MovieSerializer, Movie
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


class CastList(generics.ListCreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class CastDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def show_movies(request):
    queryset = Movie.objects.all()
    movie_list = [render_to_string("movie_thumbnail.html", {"name": movie.title, "synopsis": movie.synopsis}) for movie in queryset]
    return render(request, 'movies.html', {'movies': movie_list})

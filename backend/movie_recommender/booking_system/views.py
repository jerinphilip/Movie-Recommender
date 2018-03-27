from rest_framework import generics
from .serializers import CastSerializer, Cast, MovieSerializer, Movie
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .filters import UserFilter
from django.http import HttpResponse
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





def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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

def search(request):
    movie_list = Movie.objects.all()
    for movie in movie_list:
        print("<{}>".format(movie.title))
    print(movie_list)
    movie_filter = UserFilter(request.GET, queryset=movie_list)
    print(movie_filter.qs)
    return render(request, 'movie_list.html', {'filter': movie_filter})


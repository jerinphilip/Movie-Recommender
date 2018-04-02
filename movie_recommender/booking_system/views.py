from rest_framework import generics
from .serializers import CrewSerializer, CrewProfile, MovieSerializer
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict
import json
#from booking_system.models import Genre
from django.contrib.auth.models import User
from django.shortcuts import render
from .filters import UserFilter
#import django_filters
from itertools import chain
from .forms import UserProfileCreationForm
from django.core.exceptions import ViewDoesNotExist
from functors.booker import Booker
from functors.recommender import PopularRecommender, CBRecommender
# Create your views here.


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


# class CastList(generics.ListCreateAPIView):
#     queryset = Cast.objects.all()
#     serializer_class = CastSerializer
#
#
# class CastDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cast.objects.all()
#     serializer_class = CastSerializer
#
#
# class MovieList(generics.ListCreateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_profile = UserProfile(user=user, gender=Gender.objects.get(id=0))
            user_profile.save()
            return redirect('show_movies')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def search(request):
    movie_list = Movie.objects.all()
    #for movie in movie_list:
     #   print("<{}>".format(movie.title))
    #print(movie_list)
    movie_filter = UserFilter(request.GET, queryset=movie_list)
    #print(movie_filter.qs)
    return render(request, 'movie_list.html', {'filter': movie_filter})


def show_movies(request):
    movies = Movie.objects.all()
    #movie_list = [render_to_string("movie_thumbnail.html", MovieSerializer(movie).data) for movie in queryset]
    return render(request, 'movies.html', {'movies': movies})


def show_cast(request):
    if request.method == "POST":
        return HttpResponse("Only supports GET request")

    _crew = CrewProfile.objects.all()
    return render(request, 'cast.html', {'crews': _crew})
    # cast = CrewProfile.objects.get(id=cast_id)
    # cast_data = CrewSerializer(cast)

    # movie_list = cast.movie_set.all()
    # movie_list = [render_to_string("movie_thumbnail.html", MovieSerializer(movie).data) for movie in movie_list]

    # return render(request, 'cast.html', {"cast": cast_data.data, "movies": movie_list})

def running(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def upcoming(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def payment(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')


def book_show(request, show_id):
    booker = Booker()
    show = Show.objects.get(pk=show_id)
    seats = booker.retrieve(show)
    num_rows = len(set([i.row_id for i in seats]))
    num_cols = len(set([i.col_id for i in seats]))
    matrix = [[{"selected": True} for i in range(num_rows)] for i in range(num_cols)]

    for seat in seats:
        row_id = ord(seat.row_id) - ord('A')
        col_id = int(seat.col_id) - 1
        matrix[col_id][row_id] = {
            "selected": False,
            "id": seat.id,
        }

    return render(request, "book_show.html", {
        'show': show,
        'movie': show.movie,
        'matrix': matrix,
        })

def start_booking(request, show_id):
    show = Show.objects.get(pk=show_id)
    user = request.user.userprofile
    booker = Booker()
    booking = booker.start_booking(show, user)
    return JsonResponse({"booking": model_to_dict(booking)})

def cancel_booking(request, booking_id):
    user = request.user.userprofile
    booking = Booking.objects.get(pk=booking_id)
    if (booking.user != user):
        return JsonResponse({"success": False})
    booker = Booker()
    booker.cancel(booking)
    return JsonResponse({})

def add_seat(request, booking_id):
    seat_id = request.GET.get('seat_id')
    booker = Booker()
    Booker.select(booker, booking_id, seat_id, request.user.userprofile.id)
    return JsonResponse({})

def delete_seat(request, booking_id):
    seat_id = request.GET.get('seat_id')
    booker = Booker()
    booker.deselect(booking_id, seat_id, request.user.userprofile.id)
    return JsonResponse({})

def proceed(request):
    booking_id = request.GET.get("booking_id")
    if Booking.objects.filter(pk=booking_id).count():
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

def movie(request, movie_id):
    try:
        _movie = Movie.objects.get(pk=movie_id)
        return render(request, 'movie.html', {"movie": _movie})
    except Movie.DoesNotExist:
        return HttpResponseNotFound('<h1>Movie Does not exist</h1>')

def confirm_booking(request, show_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def crew(request, crew_id):
    try:
        _crew = CrewProfile.objects.get(pk=crew_id)
        _crew_type = Crew.objects.get(profile=crew_id)
        _movies = Movie.objects.filter(crew=_crew_type.id)
        return render(request, 'crew_profile.html', {"crew": _crew, "crew_type" : _crew_type, "movies": _movies})
    except CrewProfile.DoesNotExist:
        return HttpResponseNotFound('<h1>Crew profile Does not exist</h1>')

def theater(request, theater_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def popular(request):
    recommender = PopularRecommender()
    ordered = recommender.top(5)
    # print(ordered)
    return render(request, 'popular.html', {"popular": ordered})
    # return HttpResponseNotFound('<h1>Page under construction?</h1>')

def similar(request, movie_id):
    query = Movie.objects.get(id=movie_id)
    recommender = CBRecommender()
    ordered = recommender.top(query)
    return render(request, 'popular.html', {"popular": ordered})
    # return HttpResponseNotFound('<h1>Page under construction?</h1>')

def popular_by_genre(request, genre):
    recommender = PopularRecommender()
    ordered = recommender.top_by_genre(genre, 5)
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def shows(request, movie_id):
    _shows = Show.objects.filter(movie=movie_id)
    # print(_shows[0].show_time)
    return render(request, 'shows.html', {"shows": _shows})
    # return HttpResponseNotFound('<h1>Page under construction?</h1>')
from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.authtoken import views as drf_views

# urlpatterns = [
#     url(r'cast/$', views.CastList.as_view()),
#     url(r'movie/$', views.MovieList.as_view()),
#     url(r'cast/(?P<pk>[0-9]+)/$', views.CastDetail.as_view()),
#     url(r'^auth$', drf_views.obtain_auth_token, name='auth'),
# ]
# 
# urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = [
    path('', views.show_movies, name='index'),
    url(r'cast/(?P<cast_id>\d+)/$', views.show_cast, name='show_cast'),
    path('running', views.running, name='running'),
    path('upcoming', views.upcoming, name='running'),
    path('book/<int:show_id>/', views.book_show, name='book_show'),
    path('movie/<int:movie_id>/', views.movie, name='movie'),
    path('book/<int:show_id>/confirm', views.confirm_booking, name='confirm_booking'),
    path('payment/', views.payment, name='payment'),
    path('crew/<int:crew_id>/', views.crew, name='crew'),
    path('theater/<int:theater_id>/', views.theater, name='theater'),

]



from django.conf.urls import url
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
    url('', views.show_movies, name='index')
]



from django.urls import path, re_path
from django.conf.urls import  url
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    re_path(r"index/$", views.index, name="index"),
    re_path(r"search/$",views.search,name='search'),
    re_path(r"upload/$",views.upload,name='upload/'),
    re_path(r"changepreferences/$",views.changepreferences,name='changepreferences/'),
    #re_path(r"^destination/'%20pk%3Drow.pk$",views.destination,name="destination/")
    url(r"^destination/(?P<pk>\d+)/$",views.destination,name="destination/"),
]

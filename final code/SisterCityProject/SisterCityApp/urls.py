# howdy/urls.py
from django.conf.urls import url
from SisterCityApp import views



urlpatterns = [
    url(r'^$', views.homePage),
	url(r'^getSisterCities/$', views.searchCity),
    url(r'^getSisterCities/getSpecificCity/$', views.searchSpecific),
        url(r'^getSpecificCity/$', views.searchSpecific),
		url(r'^getSisterCities/index.html/$', views.homePage),
url(r'^getSisterCities/getSpecificCity/index.html/$', views.homePage),

]
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<sensor_id>\d+)/humidity/$', views.humidity, name='humidity'),
    url(r'^(?P<sensor_id>\d+)/temp/$', views.temperature, name='temperature'),
    url(r'^(?P<sensor_id>\d+)/light/$', views.light, name='ambient_light'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/edit$', views.edit, name='edit'),
    url(r'^create$', views.create, name='create'),
    url(r'^(?P<pk>\d+)/toggle$', views.toggle, name='toggle_outlet'),
    url(r'^(?P<pk>\d+)/delete$', views.delete, name='delete_outlet'),
]


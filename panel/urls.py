from django.urls import path

from . import views

app_name = 'panel'
urlpatterns = [
    path('', views.index, name='index'),
]
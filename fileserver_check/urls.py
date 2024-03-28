from django.urls import path

from . import views

app_name = 'fileserver_check'
urlpatterns = [
    path('', views.index, name='index'),
    path('process_files/', views.process_files, name='process_files'),
    
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'account'
urlpatterns = [
    path('login/', views.login_request, name='login'),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('register/', views.register_request, name='register'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uuid:key>', views.reset_password, name='reset_password'),
    
]
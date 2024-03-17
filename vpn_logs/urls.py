from django.urls import path

from . import views

app_name = 'vpn_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('save_text_files/', views.save_text_files, name='save_text_files'),
    path('inspect_package/<uuid:key>', views.inspect_package, name='inspect_package'),
    path('process_text_files/<uuid:key>', views.process_text_files, name='process_text_files'),
    
    
]
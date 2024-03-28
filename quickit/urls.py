from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('panel.urls'), name="panel"),
    path('account/', include('account.urls'), name="account"),
    path('vpn_logs/', include('vpn_logs.urls'), name="vpn_logs"),
    path('fileserver_check/', include('fileserver_check.urls'), name="fileserver_check"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
else:
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
# Configure Admin Titles
admin.site.site_header = "QUICKIT Yönetim Paneli"
admin.site.site_title = "QUICKIT Yönetim Paneli"
admin.site.index_title = "QUICKIT Yönetim Paneline Hoşgeldiniz"
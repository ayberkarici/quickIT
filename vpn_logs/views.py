from django.shortcuts import render, redirect
from .models import TextFile, Package
import csv
from io import StringIO
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import os
import zipfile
import chardet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import archive_logs


# Create your views here.

@login_required(login_url='account:login')
def index(request): 
    user_packages = Package.objects.filter(user=request.user).order_by("-upload_time")
    

    context = {
        "nav_name" : "vpn_logs",
        'user_packages': user_packages,
    }
    
    return render(request, 'vpn_logs/index.html', context)


@login_required(login_url='account:login')
def save_text_files(request):
    if request.method == 'POST':
        # Kullanıcının yüklediği dosyaları al
        uploaded_files = request.FILES.getlist('txt_files')
        package_name = request.POST.get('package_name')
        
        # Her bir dosya için bir TextFile nesnesi oluştur
        for uploaded_file in uploaded_files:
            text_file = TextFile.objects.create(
                file=uploaded_file,
                user=request.user,
                name=uploaded_file.name
            )
        
        # Yeni bir paket oluştur ve text dosyalarını bu pakete bağla
        package = Package.objects.create(user=request.user, name=package_name)
        package.text_files.set(TextFile.objects.filter(user=request.user, package=None))
        
        messages.success(request, 'Dosyalar başarıyla kaydedildi.')
        return redirect('vpn_logs:index')
    
    return render(request, 'save_text_files.html')


@login_required(login_url='account:login')
def inspect_package(request, key):
    # Get the package with the given key, use try-except to catch the exception if the package does not exist
    try:
        package = Package.objects.get(uuid=key)
        
        if package.user != request.user:
            return JsonResponse({'error': 'Bu paketi inceleme yetkiniz yok'}, status=403)
        
        # Get the text files of the package #
        text_files = package.text_files.all()
            
    except Package.DoesNotExist:
        return JsonResponse({'error': 'Paket bulunamadı'}, status=404)
    
    context = {
        "nav_name" : "vpn_logs",
        "package" : package,
        "text_files" : text_files,
    }
    return render(request, 'vpn_logs/inspect_vpn_logs.html', context)


@login_required(login_url='account:login')
def process_text_files(request, key):
    try:
        package = Package.objects.get(uuid=key)
    except Package.DoesNotExist:
        return JsonResponse({'error': 'Paket bulunamadı'}, status=404)

    if package.user != request.user:
        return JsonResponse({'error': 'Bu paketi inceleme yetkiniz yok'}, status=403)

    # Text dosyalarını al
    text_files = TextFile.objects.filter(package=package)
    
    
    # Dosyaları geçici bir klasöre kaydetmeden işleme geç
    archive_directory = settings.TEMP_DIRECTORY  # Arşiv klasörü
    zip_file_path = archive_logs(text_files, archive_directory)
    print(f'Arşiv dosyası oluşturuldu: {zip_file_path}')

    # Zip dosyasını kullanıcıya indirme olarak sun
    with open(zip_file_path, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_file_path)}'
        return response


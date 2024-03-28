from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import pandas as pd
from .utils import *

# Create your views here.

@login_required(login_url='account:login')
def index(request): 
    
    context = {
        "nav_name" : "tools",
        "sub_nav" : "fileserver_check"
    }
    
    return render(request, 'fileserver_check/index.html', context)

@login_required(login_url='account:login')
def process_files(request):
    try:
        # Dosyaları al
        search_results = request.FILES['search_results']
        file_server = request.FILES['file_server']
        
        # Dosyaları satır satır oku ve işle
        active_emails = [process_email(email.decode('utf-8').strip()) for email in search_results]
        file_server_names = [process_file_server_name(name.decode('utf-8').strip()) for name in file_server]

        # Eşleşmeyenleri bul
        mismatched_emails = []
        for email_parts in active_emails:
        
            matched = False
            for file_name_parts in file_server_names:
                if email_parts == file_name_parts:
                    matched = True
                    break
            if not matched:
                mismatched_emails.append(email_parts)
        
        context = {
            'success': 'true',
            'mismatched_emails': mismatched_emails
        }

        return JsonResponse(context, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

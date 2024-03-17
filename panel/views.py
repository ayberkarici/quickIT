from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='account:login')
def index(request):
    
    context = {
        "nav_name" : "home"
    }
    
    return render(request, 'panel/index.html', context)

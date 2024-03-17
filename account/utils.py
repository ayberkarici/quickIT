import re
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.files.images import get_image_dimensions
import uuid

def validate_password(request, password):
    # Check if the password is empty
    if not password:
        messages.warning(request, "Şifre boş olamaz.")
        return False

    if 8 > len(password):
        messages.warning(request, "Şifre en az 8 karakter olmalıdır.")
        return False

    # Check if the password contains any characters that are not allowed
    allowed_characters = '0123456789_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.'
    for character in password:
        if character not in allowed_characters:
            messages.warning(request, "Şifre sadece harf, rakam ve alt çizgi içerebilir.")
            return False

    # Check if the password contains at least one capital letter
    if not any(c.isupper() for c in password):
        messages.warning(request, "Şifre en az bir büyük harf içermelidir.")
        return False

    # If the password passes all checks, return True
    return True

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
    
def form_errors (request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.warning(request, f'{error}')
            
    # Hata mesajlarını form nesnesine ekleyin
    for field, errors in form.errors.items():
        for error in errors:
            last_class = form[field].field.widget.attrs.get('class')
            form[field].field.widget.attrs.update({'class': f'{last_class} is-invalid'})
    
def rival_form_errors (request, form):
    # Hata mesajlarını form nesnesine ekleyin
    for field, errors in form.errors.items():
        for error in errors:
            messages.warning(request, f'{form[field].field.label}, {error}')
            last_class = form[field].field.widget.attrs.get('class')
            form[field].field.widget.attrs.update({'class': f'{last_class} is-invalid'})
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.core.validators import validate_email
from django.conf import settings
import uuid
from .utils import *
from django.utils import timezone

# Create your views here.

current_date = timezone.now()

class CustomLogoutView(LogoutView):
    next_page = 'account:login'

def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if the user is already has a user, if so check if the user has a profile
                if not Profile.objects.filter(user=user).exists():
                    Profile.objects.create(user=user)
    
                login(request, user)
                messages.success(request, f'Hoş geldin, {username}!')
                return redirect('panel:index')  # Kullanıcı başarıyla oturum açtıktan sonra yönlendirme
            else:
                messages.warning(request, 'Geçersiz Kullanıcı Adı veya Şifre.')
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, f'{field.capitalize()}: {error}')

        else: 
            # Hata mesajlarını form nesnesine ekleyin
            for field, errors in form.errors.items():
                for error in errors:
                    form[field].field.widget.attrs.update({'class': 'form-control is-invalid'})
                    form[field].field.widget.attrs.update({'placeholder': error})
    else:
        form = LoginForm()
        
    return render(request, 'account/login.html', {'form': form})

def register_request (request):
    if request.user.is_authenticated:
        return redirect('panel:index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')

            if email:
                user.email = email
            
            user.save()
            
            Profile.objects.filter(user=user)
            
            messages.success(request, "Başarıyla kayıt oldun! Giriş yap ve maceraya başla!" )
            return redirect('account:login')
    
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f'{error}')
            
            # Hata mesajlarını form nesnesine ekleyin
            for field, errors in form.errors.items():
                for error in errors:
                    last_class = form[field].field.widget.attrs.get('class')
                    form[field].field.widget.attrs.update({'class': f'{last_class} is-invalid'})
                    
    else:
        form = RegisterForm()
        
    return render(request, 'account/register.html', {'form': form})

def forgot_password (request):
    if request.method == 'POST':
        form = RecoveryForm(request.POST)
        form_errors(request, form)

        if form.is_valid():
            user_email = request.POST['email'].strip()

            if MailConfirmList.objects.filter(user_instance__email=user_email, expire_date__gte=current_date).exists():
                messages.warning(request, "Zaten bir kurtarma emaili almışsınız. Lütfen gelen kutunuzu kontrol edin.")
                return redirect('account:forgot_password')
                
            if User.objects.filter(email=user_email).exists(): 
                user_instance = User.objects.get(email=user_email)
                confirm_no = uuid.uuid4()
                CURR_HOST = request.get_host()
            
                link = f"{CURR_HOST}/account/reset-password/{confirm_no}"
                
                message_to_user = f'Aşağıdaki linke tıkladıktan sonra açılan sayfadan şifreni değiştirebilirsin. Bu link 2 dakikalığına geçerlidir.  \n\n {link} \n\n Eğer bu işlemi sen gerçekleştirmemişsen bu emaili görmezden gelebilirsin. \n\n Saygılarımızı sunarız, \n keysnapp.com'
                
                try:                   
                    MailConfirmList.objects.create(
                        user_instance=user_instance,
                        confirm_no=confirm_no
                    )
                except Exception as ex :
                    messages.warning(request, "Emailinizi işlerken bir sorun oluştu. Lütfen tekrar deneyin.")
                    return redirect('account:forgot_password')
                
                try:
                    send_mail(
                        '🔐 www.keysnapp.com şifremi unuttum. ',
                        message_to_user,
                        settings.EMAIL_HOST_USER,
                        [user_email,],
                        fail_silently=False,
                    )
                except Exception as ex:
                    print(ex)
                    messages.warning(request, "Emailiniz gönderilirken bir sorun oluştu. Lütfen tekrar deneyin.")
                    return redirect('account:forgot_password')

                messages.success(request, "Emailiniz başarıyla gönderildi. Lütfen 2 dakika içinde şifrenizi yenileyin.")
                return redirect('account:forgot_password')
                    
            else:
                messages.warning(request, "Bu email adresiyle kayıtlı bir kullanıcı bulunamadı.")
                return redirect('account:forgot_password')
        
    else:
        form = RecoveryForm()
        
    return render(request, 'account/forgot-password.html', {'form': form})

def reset_password (request, key):
    if request.method == 'POST':
        form = DoRecoveryForm(request.POST)
        form_errors(request, form)
        
        new_password1 = request.POST['password'].strip()
        new_password2 = request.POST['confirm-password'].strip()
        
        user = MailConfirmList.objects.get(confirm_no=key).user_instance
        mail_conf = MailConfirmList.objects.get(confirm_no=key)

        if new_password1 != new_password2:
            messages.warning(request, "Şifreler eşleşmiyor.")
            return render(request, 'account/reset-password.html', {'key': key, 'form': form, 'curr_user': user})
        
        try: 
           MailConfirmList.objects.filter(confirm_no=key, expire_date__gte=current_date).exists() 
        except:
            print('MailConfirmList error')
            messages.warning(request, "Geçersiz token. Lütfen tekrar deneyin.")
            return redirect("account:forgot_password")
           
        if is_valid_uuid(key) and not MailConfirmList.objects.get(confirm_no=key).is_used:
            try:
                confirm_instance = MailConfirmList.objects.get(confirm_no=key)
                user_instance = User.objects.get(id=confirm_instance.user_instance.id)
            except Exception as ex:
                messages.warning(request, "Geçersiz token. Lütfen tekrar deneyin.")
                return redirect("account:forgot_password")

            if user_instance is None:
                messages.warning(request, "Bu email adresiyle kayıtlı bir kullanıcı bulunamadı.")
                return redirect("account:forgot_password")
        
            new_password = request.POST['password'].strip()
            
            if validate_password(request, new_password):
                try:
                    try_user = authenticate(request, username=user_instance.username, password=new_password)
                except Exception as ex:
                    try_user = None
                    
                if try_user is None:
                    # Set the new password
                    try:
                        user_instance.set_password(new_password)
                        user_instance.save()
                    except Exception as ex:
                        messages.warning(request, "Şifreniz değiştirilemedi. Lütfen tekrar deneyin.")
                        return render(request, 'account/reset-password.html', {'key': key, 'form': form, 'curr_user': user, 'mail_conf': mail_conf})

                    
                    confirm_instance.is_used = True
                    confirm_instance.save()
                    
                    # Set the log out
                    try:
                        logout(request)
                    except Exception as ex:
                        print(ex)
                        

                    # Go to login to log in
                    messages.success(request, "Şifreniz başarıyla değiştirildi. Lütfen giriş yapın.")
                    return redirect("account:login")
                
                else:   
                    messages.warning(request, "Şifreniz eskisiyle aynı olamaz. Lütfen tekrar deneyin.")
                    return render(request, 'account/reset-password.html', {'key': key, 'form': form, 'curr_user': user, 'mail_conf': mail_conf})

            messages.warning(request, "Lütfen geçerli bir şifre girin.")
            return render(request, 'account/reset-password.html', {'key': key, 'form': form, 'curr_user': user, 'mail_conf': mail_conf})

        messages.warning(request, "Geçersiz token. Lütfen tekrar deneyin.")
        return redirect("account:forgot_password")

    else:
        mail_conf = MailConfirmList.objects.get(confirm_no=key)
        user = MailConfirmList.objects.get(confirm_no=key).user_instance
        
        if MailConfirmList.objects.filter(confirm_no=key, expire_date__lte=current_date).exists():
            messages.warning(request, "Bu kurtarma linkinin tarihi geçmiş. Lütfen daha sonra tekrar deneyin.")
            return redirect('account:forgot_password')
        
        if not is_valid_uuid(key):
            messages.warning(request, "Yanlış bir anahtar girdiniz. Lütfen doğru email adresini girin.")
            return redirect('market:forgot_password')
        
        form = DoRecoveryForm(user)
    
    return render(request, 'account/reset-password.html', {'key': key, 'form': form, 'curr_user': user, 'mail_conf': mail_conf})

    
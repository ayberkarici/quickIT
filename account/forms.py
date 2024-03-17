from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Kullanıcı Adı",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Kullanıcı adını veya email adresini gir'})
    )
    password = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'············', 'aria-describedby':'password'})
    )

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Kullanıcı Adı",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Kullanıcı adını gir'})
    )
    shop_name = forms.CharField(
        label="Mağaza İsmi",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mağaza ismini gir'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Emailini gir'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'············'})
    )
    password2 = forms.CharField(
        label="Password Onay",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'············'})
    )
    
    policy = forms.BooleanField(
      label="Policy Checkbox", 
      widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type':'checkbox', 'name':'terms'}), 
      required=True,
    )
    
    error_css_class = 'text-error'  
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        try : 
            validate_email(email)
        except ValidationError:
            raise ValidationError("Geçersiz email")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("Böyle bir email zaten var.")
        
        return email

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="New Password Verification",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class DoRecoveryForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="Yeni Şifre",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Yeni Şifre Onayı",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    
class RecoveryForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email ",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'example@gmail.com'})
    )



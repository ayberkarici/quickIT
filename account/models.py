from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_accepted_policy = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=True)

    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class ContactMessages(models.Model):
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    message = models.TextField(max_length=600, blank=True)
    
class MailConfirmList(models.Model):
    user_instance = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    confirm_no = models.CharField(max_length=56, blank=False, null=False)
    is_used = models.BooleanField(default=False, blank=False, null=False)
    expire_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Yeni bir ürünse
            self.deals_end_date = datetime.now() + timedelta(minutes=2)
        
        super(MailConfirmList, self).save(*args, **kwargs)
    

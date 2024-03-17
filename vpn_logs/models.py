from django.db import models
from django.contrib.auth.models import User
import uuid

class TextFile(models.Model):
    file = models.FileField(upload_to='text_files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    package = models.ForeignKey('Package', related_name='text_files', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.file.url}"

class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField(default=0)
    name = models.CharField(max_length=100, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    

    def __str__(self):
        clear_upload_time = self.upload_time.strftime("%d/%m/%Y %H:%M:%S")
        
        return f"Package uploaded by {self.user.username} at {clear_upload_time}"

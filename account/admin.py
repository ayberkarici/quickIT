from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_created_at')

    def get_created_at(self, obj):
        return obj.user.date_joined 

    get_created_at.short_description = 'User Created At'  # Admin arayüzünde görüntülenecek kısa açıklama



admin.site.register(Profile, ProfileAdmin)
admin.site.register(MailConfirmList)
admin.site.register(ContactMessages)

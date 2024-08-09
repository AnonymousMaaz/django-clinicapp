from django.contrib import admin
from .models import UserProfile, MedicalRecord

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'problem')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)

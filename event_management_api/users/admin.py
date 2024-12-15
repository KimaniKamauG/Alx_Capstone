from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    list_display = ['email']

# Register your models here.
admin.site.register(CustomUser, UserAdmin) 
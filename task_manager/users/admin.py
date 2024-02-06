from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm
from .models import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = RegistrationForm

admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.

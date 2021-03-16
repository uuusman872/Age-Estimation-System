from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser,Doctor,Patient
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Patient)


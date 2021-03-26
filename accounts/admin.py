from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser,Doctor,Patient
from django.conf import settings
from mapbox_location_field.admin import MapAdmin  
from .models import SomeLocationModel  
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Doctor )
admin.site.register(Patient)
admin.site.register(SomeLocationModel, MapAdmin)


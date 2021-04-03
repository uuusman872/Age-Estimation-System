from django.db import models
from django.contrib.auth.models import AbstractUser  
from mapbox_location_field.models import LocationField

class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient =models.BooleanField(default=False)
    is_approve =models.BooleanField(default=False)
    first_name= models.CharField( max_length=50)
    last_name= models.CharField( max_length=50)
    phone_number= models.CharField( max_length=50)
    email = models.EmailField(max_length= 50)
    profile_image = models.ImageField(default="ASD.jpg" , blank= True, null= True)

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    Cnic = models.CharField( max_length=50)
    
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    medical_history= models.CharField( max_length=50)
    age= models.CharField( max_length=50)

class SomeLocationModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    location = LocationField(map_attrs={"rotate": True, "marker_color": "blue", })
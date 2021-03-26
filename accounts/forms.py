from .models import Doctor, Patient , CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect , HttpResponse
from django.views.generic import View
from django import forms
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utilts import account_activation_token
from .models import SomeLocationModel
from mapbox_location_field.models import LocationField
class ProfileForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = [
         'profile_image'
        ]
    
class LocationForm(forms.ModelForm):
    location = LocationField()
    class Meta:  
        model = SomeLocationModel 
        fields = [
            'location'
        ]
        


class DoctorForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number= forms.CharField( required = True)
    email = forms.EmailField(required=True)
    Cnic = forms.CharField( required = True)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
    
    # def cleaasdasdn_username(self):
    #     user = self.cleaned_data['username']
    #     try:
    #         match = CustomUser.objects.get(username=user)
    #     except:
    #         return self.cleaned_data['username']
    #     raise forms.ValidationError("dasssssssssssssssssssssssssssssssssssssssssssssssss")


    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.is_doctor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.is_active = False
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.Cnic = self.cleaned_data.get('Cnic')
        doctor.save()
        return user






class PatientForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number= forms.CharField( required = True)
    medical_history= forms.CharField(required = True)
    age= forms.CharField( required = True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser

    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.is_patient = True
        user.is_approve = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        patient = Patient.objects.create(user=user)
        patient.medical_history = self.cleaned_data.get('medical_history')
        patient.age = self.cleaned_data.get('age')
        patient.save()
        return user
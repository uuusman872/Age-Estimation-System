from .models import Doctor, Patient , CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError


from django import forms

class DoctorForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number= forms.CharField( required = True)
    Cnic = forms.CharField( required = True)
    location= forms.CharField( required = True)


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
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.Cnic = self.cleaned_data.get('Cnic')
        doctor.location = self.cleaned_data.get('location')
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
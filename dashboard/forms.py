from django import forms
from .models import PatientRecord
#DataFlair
class PatientCreate(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = '__all__'
 
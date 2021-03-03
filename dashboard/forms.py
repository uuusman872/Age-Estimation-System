from django import forms
from .models import patient
#DataFlair
class PatientCreate(forms.ModelForm):
    class Meta:
        model = patient
        fields = '__all__'
 
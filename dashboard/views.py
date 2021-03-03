from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import patient
from .forms import PatientCreate

# Create your views here.

@login_required
def doctor_dashboard(request):
    patients=patient.objects.all()
    context = {
        'patients' : patients
    }
    return render(request,"doctor/doctor_dashboard.html", context)
@login_required
def doctor_form(request):
    form= PatientCreate()
    if request.method == 'POST':
        form=PatientCreate(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doctor_table')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        context= {'form': form}
        return render(request,"doctor/doctor_form.html" , context)

def update(request, patient_id):
    patient_id = int(patient_id)
    try:
        get_patient = patient.objects.get(id = patient_id)
    except patient.DoesNotExist:
        return redirect('doctor_table')
    form = PatientCreate( instance = get_patient)
    if request.method == 'POST':
        form = PatientCreate(request.POST or None,request.FILES, instance = get_patient)
        if form.is_valid():
            form.save()
            return redirect('doctor_table')
    return render(request, "doctor/doctor_form.html", {'form':form})

        
@login_required
def doctor_table(request):
    patients=patient.objects.all()
    context = {
        'patients' : patients
    }
    return render(request,"doctor/doctor_table.html" , context)

@login_required
def age_estimation(request):
    return render(request,"doctor/age-estimation.html")

def delete(request, patient_id):
    patient_id = int(patient_id)
    try:
        get_patient = patient.objects.get(id = patient_id)
    except patient.DoesNotExist:
        return redirect('doctor_table')
    get_patient.delete()
    return redirect('doctor_table')



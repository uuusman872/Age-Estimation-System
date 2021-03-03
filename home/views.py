from django.shortcuts import render,HttpResponse

# Create your views here.

def index(request):
    return render(request,"index.html")

def services(request):
    return render(request,"services.html")

def services1(request):
    return render(request,"services1.html")


from django.contrib import admin
from django.urls import path,include
from accounts import views
from.views import VerificationView

urlpatterns = [


    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('doctor_register', views.doctor_register.as_view(), name="doctor_register"),
    path('patient_register', views.patient_register.as_view(), name="patient_register"),

    path('profile', views.profile, name="profile"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name="activate"),
]
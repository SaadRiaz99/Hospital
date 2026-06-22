from django.shortcuts import render, redirect
from app.models import signup as SignupModel
from app.models import Appointment as AppointmentModel
from app.models import Login as LoginModel
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
import datetime

# Create your views here.
def home(request):
    return render(request, 'Index.html')

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        father_name = request.POST.get('Father_name')
        cnic = request.POST.get('Cnic')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        dob = request.POST.get('dob')

        signup_entry = SignupModel(
            first_name=first_name,
            father_name=father_name,
            cnic=cnic,
            phone=phone,
            email=email,
            dob=dob
        )
        signup_entry.save()
    return render(request, 'signup.html')

def Feature(request):
    return render(request, 'Feature.html')

def Services(request):
    return render(request, 'Services.html')

def Doctor_Detail(request):
    return render(request, 'Doctor_Detail.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        # check if email already exists (signup flow)
        if LoginModel.objects.filter(Email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect('signup')

        # create and persist the login entry
        login_entry = LoginModel.objects.create(
            Email=email,
            password=password,
        )
        return redirect('patient')

    # For GET (and other) requests just render the page
    return render(request, 'login.html')
 
def Appointment(request):
    if request.method == "POST":
        patient_name = request.POST.get('patient_name')
        Email = request.POST.get('email')
        Phone = request.POST.get('phone')
        Doctor = request.POST.get('doctor')
        Date = request.POST.get('date')
        message = request.POST.get('message')

        appointment = AppointmentModel(
            patient_name=patient_name,
            Email=Email,
            Phone=Phone,
            Doctor=Doctor,
            Date=Date,
            message=message,
        )
        appointment.save()
    return render(request, 'Appot.html')

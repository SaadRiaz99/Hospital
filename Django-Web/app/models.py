from django.db import models

# `Service` model removed per request.
class signup(models.Model):
    
    first_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    cnic = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.first_name


class Appointment(models.Model):
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.EmailField(null=True, blank=True)
    Phone = models.CharField(max_length=15, null=True, blank=True)  
    Doctor = models.CharField(max_length=100, null=True, blank=True)
    Date = models.DateField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.patient_name


class Login(models.Model):
    Email = models.EmailField(max_length=100, null=True , blank=True)
    password = models.CharField(max_length=100, null=True , blank=True)
    def __str__(self):
        return self.Email      
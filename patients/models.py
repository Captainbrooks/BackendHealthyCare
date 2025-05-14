from django.db import models
from authentication.models import User
from appointments.models import PatientAppointment
import datetime

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    blood_type = models.CharField(max_length=5, null=True, blank=True)
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.full_name


class PatientHistory(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    surgeries = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"History of {self.patient.full_name}"


class TestResult(models.Model):
    patient = models.ForeignKey(Patient,  related_name='test_results', on_delete=models.CASCADE)
    test_type = models.CharField(max_length=100)
    result = models.TextField()
    date = models.DateField()
    doctor = models.ForeignKey('doctors.Doctors', on_delete=models.SET_NULL, null=True)
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.test_type} for {self.patient.full_name} on {self.date}"


class VitalSign(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    blood_pressure = models.CharField(max_length=20)
    pulse = models.IntegerField()
    temperature = models.FloatField()
    weight = models.FloatField()
    
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Vitals for {self.patient.full_name} on {self.date}"


class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    
    
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} for {self.patient.full_name}"


class AppointmentDiscussion(models.Model):
    appointment = models.ForeignKey(Patient, on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return f"Discussion for {self.appointment}"

    
    

    

    
    
    

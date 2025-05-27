from django.db import models
from datetime import date
from doctors.models import Doctors, TimeSlot


class PatientAppointment(models.Model):
    
    STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('in-progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    department_name = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    booking_date = models.DateField(default=date.today)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='new_appointments')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    reason_to_visit = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.timeslot.is_booked = True
            self.timeslot.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Patient: {self.patient.full_name} - Booked on {self.booking_date} - for  {self.timeslot}"
    
    class Meta:
        unique_together = ('doctor', 'timeslot')


class UserMessages(models.Model):
    
    DEPARTMENT_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('General Medicine', 'General Medicine'),
        ('Dermatology', 'Dermatology'),
        ('Dentistry', 'Dentistry'),
        ('Ophthalmology', 'Ophthalmology')
        
]
    
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default='General Medicine',
    )
    message = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.fullname} has {self.message} for {self.department}"
    

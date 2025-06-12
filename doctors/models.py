from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField
from cloudinary.models import CloudinaryField


# Create your models here.



class Hospital(models.Model):
    hospital_name=models.CharField(max_length=255)
    location=models.CharField(max_length=255)

    def __str__(self):
        return self.hospital_name
    
    
class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Certification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
class Awards(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    


class Doctors(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    # Choices for department_name
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

    # Choices for availability
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    doctor_name = models.CharField(max_length=100)
    department_name = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,  # Add choices here
        default='General Medicine',  # Default department (optional)
    )
    education = models.CharField(max_length=255)
    experience = models.IntegerField()
    background=models.TextField(blank=True, null=True)
    availability = MultiSelectField(
        choices=DAY_CHOICES,  # Allow multiple days to be selected
        max_choices=7,  # You can limit the number of choices
        blank=True,  # Allow empty selection
    )
    hospital_name = models.ForeignKey('Hospital', on_delete=models.CASCADE, related_name="doctors")
    rating = models.FloatField(default=0.0)
    num_reviews = models.IntegerField(default=0)
 
    image = CloudinaryField('image', folder='healthycare-doctors')
    specializations = models.ManyToManyField(Specialization, blank=True)
    certifications = models.ManyToManyField(Certification, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    awards=models.ManyToManyField(Awards,blank=True,related_name="awarded_doctors")
    publications=models.IntegerField(default=0,blank=True, null=True)
    is_extraordinary = models.BooleanField(default=False)
    
    

    def __str__(self):
        return f"{self.doctor_name} - {self.department_name}"
    
    
    
class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name='timeslots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_date = models.DateField()
    is_booked=models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'start_time', 'end_time', 'appointment_date')

    def __str__(self):
        return f"{self.doctor.doctor_name} - {self.appointment_date} from {self.start_time} to {self.end_time}"
    
    
    
    





class Review(models.Model):
    doctor_name=models.ForeignKey(Doctors,related_name="reviews",on_delete=models.CASCADE)
    patient_name=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.patient_name.username} for {self.doctor_name.doctor_name}"
    
    
    



    
    
    
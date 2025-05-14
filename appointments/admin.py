from django.contrib import admin
from .models import PatientAppointment
from appointments.models import UserMessages

# Register your models here.

admin.site.register(PatientAppointment)
admin.site.register(UserMessages)



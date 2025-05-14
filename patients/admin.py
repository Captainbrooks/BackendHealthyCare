from django.contrib import admin
from patients.models import Patient, PatientHistory, TestResult, VitalSign,\
    Medication, AppointmentDiscussion

# Register your models here.


admin.site.register(Patient)
admin.site.register(PatientHistory)
admin.site.register(TestResult)
admin.site.register(VitalSign)
admin.site.register(Medication)
admin.site.register(AppointmentDiscussion)

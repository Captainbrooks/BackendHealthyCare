

# Register your models here.
from django.contrib import admin
from .models import Doctors, Hospital, Review
from doctors.models import Specialization, Certification, Language, Awards,\
    TimeSlot

admin.site.register(Doctors)
admin.site.register(Hospital)
admin.site.register(Review)
admin.site.register(Specialization)
admin.site.register(Certification)
admin.site.register(Language)
admin.site.register(Awards)
admin.site.register(TimeSlot)


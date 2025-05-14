from rest_framework import serializers
 
import base64
from django.core.files.base import ContentFile
import uuid
from io import BytesIO



from .models import Doctors, Specialization, Certification, Language, Review,TimeSlot,Hospital, Review,Awards
from appointments.models import PatientAppointment


class TimeSlotSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=TimeSlot
        fields= ['id', 'start_time', 'end_time', 'appointment_date']
        
            
        




class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['name']

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']
        
class ReviewSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    

    class Meta:
        model = Review
        fields = ['doctor_name', 'patient_name', 'rating', 'review_text', 'date','patient']


class HospitalSerializer(serializers.ModelSerializer):
    
    
   
    class Meta:
        model=Hospital
        fields='__all__'
        
class AwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Awards
        fields='__all__'
        
class DoctorsSerializers(serializers.ModelSerializer):
    
    specializations = SpecializationSerializer(many=True)
    certifications = CertificationSerializer(many=True)
    languages = LanguageSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    hospital_name = serializers.CharField(source='hospital_name.hospital_name')
    location = serializers.CharField(source='hospital_name.location')
    awards=AwardsSerializer(many=True)
    


    class Meta:
        model = Doctors
        fields = ['id','doctor_name', 'department_name', 'education', 'experience','background', 'availability', 'hospital_name','location', 'rating', 'num_reviews', 'image','specializations', 'certifications', 'languages', 'reviews','awards','publications','is_extraordinary']





    



from rest_framework import serializers
from authentication.models import User
from .models import *
from appointments.serializers import DoctorsSerializers
from doctors.models import Doctors



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username']


        
        
        
class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientHistory
        fields= '__all__'
        
class TestResultSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctors.objects.all())
    doctor_info = DoctorsSerializers(source='doctor', read_only=True)
    
    class Meta:
        model=TestResult
        fields=['id','patient','test_type','result','date','doctor','doctor_info','report_file']
        

        
class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model=VitalSign
        fields= '__all__'
        

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medication
        fields= '__all__'
        
class AppointmentDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppointmentDiscussion
        fields= '__all__'
        
        
class PatientSerializer(serializers.ModelSerializer):
    user=serializers.CharField(source='user.username')
    test_results=TestResultSerializer(many=True,read_only=True)
    vitalsign_set = VitalSignSerializer(many=True, read_only=True)
    medication_set = MedicationSerializer(many=True, read_only=True)
    
    appointmentdiscussion_set=AppointmentDiscussionSerializer(many=True,read_only=True)
    

    
    
    class Meta:
        model=Patient
        fields=['user','id', 'full_name', 'age', 'gender', 'blood_type', 'phone', 'emergency_contact','test_results',
                'vitalsign_set',
                'medication_set',
                'appointmentdiscussion_set',
                
                ]
    

        

        
    
    
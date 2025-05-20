from rest_framework import serializers
from .models import PatientAppointment,UserMessages
from patients.models import Patient,TestResult
from doctors.models import Doctors, TimeSlot
from doctors.serializers import TimeSlotSerializer


class DoctorsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Doctors
        fields='__all__'

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=TestResult
        fields='__all__'

class PatientSerializer(serializers.ModelSerializer):
    
    test_results = TestResultSerializer(many=True, read_only=True)
    
    class Meta:
        model=Patient
        fields=['id','full_name','phone','age','gender','blood_type','emergency_contact','test_results']
        

class PatientAppointmentSerializer(serializers.ModelSerializer):
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)
    timeslot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all(), write_only=True)
    
    
    patient_data = PatientSerializer(source='patient', read_only=True)
    timeslot_data = TimeSlotSerializer(source='timeslot', read_only=True)
    

    class Meta:
        model=PatientAppointment
        fields = '__all__'
        
        
class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserMessages
        fields = '__all__'
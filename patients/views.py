from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from patients.serializers import *
from rest_framework.exceptions import NotFound
from .serializers import *
from django.views.generic.edit import CreateView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http.response import Http404


# Create your views here.





class PatientView(RetrieveAPIView):
    serializer_class = PatientSerializer

    def get_object(self):
        patient_id = self.kwargs.get('id')
        try:
            return Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise NotFound("Patient history not found.")
        
        
        
class TestResultCreateView(generics.CreateAPIView):
    
    queryset=TestResult.objects.all()
    serializer_class=TestResultSerializer
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            patient_id=serializer.validated_data['patient'].id
            patient = Patient.objects.get(id=patient_id)
            
            return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
        
        
class TestResultDeleteView(generics.DestroyAPIView):

    serializer_class=TestResultSerializer
    
    def get_object(self):
        patient_id = self.kwargs.get('patientId')  
        test_id = self.kwargs.get('test_id')  
        
        print("patient_id", patient_id)
        print("test_id", test_id)
        
        if not patient_id or not test_id:
            raise ValueError("Both patient_id and test_id are required.")

        try:
            return TestResult.objects.get(patient__id=patient_id, id=test_id)
        except TestResult.DoesNotExist:
            raise Http404("Test result not found.")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Test result deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class VitalSignsCreateView(generics.CreateAPIView):
    queryset = VitalSign.objects.all()
    serializer_class = VitalSignSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print(serializer.errors)  # Print what went wrong
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        patient_id = serializer.validated_data['patient'].id
        patient = Patient.objects.get(id=patient_id)

        return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
    
    
    

        
        
class VitalSignDeleteView(generics.DestroyAPIView):

    serializer_class=VitalSignSerializer
    
    def get_object(self):
        patient_id = self.kwargs.get('patientId')  
        vital_id = self.kwargs.get('vital_id')  
        
        print("patient_id", patient_id)
        print("vital_id", vital_id)
        
        if not patient_id or not vital_id:
            raise ValueError("Both patient_id and vital_id are required.")

        try:
            return VitalSign.objects.get(patient__id=patient_id, id=vital_id)
        except VitalSign.DoesNotExist:
            raise Http404("Vital sign not found.")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Vital sign deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class MedicationCreateView(generics.CreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print(serializer.errors)  # Print what went wrong
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        patient_id = serializer.validated_data['patient'].id
        patient = Patient.objects.get(id=patient_id)

        return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
    
    
    
class MedicationDeleteView(generics.DestroyAPIView):

    serializer_class=MedicationSerializer
    
    def get_object(self):
        patient_id = self.kwargs.get('patientId')  
        medication_id = self.kwargs.get('medication_id')  
        
        print("patient_id", patient_id)
        print("vital_id", medication_id)
        
        if not patient_id or not medication_id:
            raise ValueError("Both patient_id and vital_id are required.")

        try:
            return Medication.objects.get(patient__id=patient_id, id=medication_id)
        except Medication.DoesNotExist:
            raise Http404("Medication not found.")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Medication deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class UpdateMedicationView(generics.UpdateAPIView):
    serializer_class = MedicationSerializer

    def get_object(self):
        patient_id = self.kwargs.get('patientId')
        medication_id = self.kwargs.get('medication_id')


        try:
            return Medication.objects.get(id=medication_id, patient__id=patient_id)
        except Medication.DoesNotExist:
            raise Http404("Medication not found for this patient.")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True) 

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
    
    
        
        
    
            
    
    
        
        
    
    
    
        
        
        

    


    
    
        
    

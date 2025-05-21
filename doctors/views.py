from rest_framework import generics
from .models import Doctors, Hospital, Review
from .serializers import HospitalSerializer, DoctorsSerializers, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from doctors.serializers import TimeSlotSerializer
from .models import TimeSlot
from appointments.models import PatientAppointment
from pip._vendor.urllib3.util.timeout import current_time
from rest_framework.views import APIView
from .models import Doctors
from rest_framework.response import Response
from rest_framework import status
from .serializers import DoctorsSerializers
import time



class UpdateDoctorAvailability(APIView):

    def patch(self, request, doctor_id):
        try:
            doctor = Doctors.objects.get(id=doctor_id)
        except Doctors.DoesNotExist:
            return Response({"detail": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        updated_availability = request.data.get('availability', [])
        
        doctor.availability = updated_availability
        doctor.save()
        serializer = DoctorsSerializers(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class DoctorsListCreateView(generics.ListCreateAPIView):
    queryset = Doctors.objects.all()
    serializer_class = DoctorsSerializers
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    def perform_create(self, serializer):
        # Custom logic before saving the doctor instance
        # This will handle image uploading correctly
        serializer.save()


class DoctorsListView(generics.ListAPIView):
    
    serializer_class = DoctorsSerializers
    
    def get_queryset(self):
        path = self.request.path
        queryset = self.queryset
        

        department_name = self.kwargs.get('department_name')
        doctor_name = self.kwargs.get('doctor_name')
        availabletoday = self.kwargs.get('availabletoday')
        qualified = self.kwargs.get('qualified')
        
        if doctor_name:
            doctor_name = doctor_name.replace('-', ' ')
            
        today = timezone.now().strftime('%A')
        
        queryset = Doctors.objects.all()

        if department_name:
            queryset = queryset.filter(department_name__iexact=department_name)

        if doctor_name:
            queryset = queryset.filter(doctor_name__iexact=doctor_name)
            
        if qualified:
            queryset = queryset.filter(is_extraordinary=True)
            
        if availabletoday:
            doctors_available_today = []
            
            for doctor in queryset:
                if today in doctor.availability:
                    doctors_available_today.append(doctor)
                    
            return doctors_available_today
            
        return queryset


class DoctorsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorsSerializers

    def get_queryset(self):
        return Doctors.objects.all()

    def get_object(self):
        doctor_name = self.kwargs.get('doctor_name')
        doctor_name = doctor_name.replace('-', ' ')
        
        try:
            doctor = Doctors.objects.get(doctor_name=doctor_name)
            return doctor
        except Doctors.DoesNotExist:
            raise NotFound("Doctor with the specified name not found.")
        
        
class DoctorAvailabilityView(generics.RetrieveAPIView):
    queryset = Doctors.objects.all()
    serializer_class = DoctorsSerializers
    lookup_field = 'pk'


class TimeSlotListAPIView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    
    def get_queryset(self):
        
        doctor_id = self.kwargs.get('doctor_id')
        appointment_date = self.request.query_params.get('appointment_date')
        
        timeslot = TimeSlot.objects.filter(doctor_id=doctor_id, appointment_date=appointment_date,is_booked=False)
        
        timeslot_ids = timeslot.values_list('id', flat=True)
        
        booked_timeslots = PatientAppointment.objects.filter(doctor_id=doctor_id, timeslot__in=timeslot_ids).values_list('timeslot_id', flat=True)
        
        available_timeslots = timeslot.exclude(id__in=booked_timeslots)
        
        if appointment_date == timezone.now().date().isoformat():
            current_time = timezone.now().time()
            available_timeslots = available_timeslots.filter(start_time__gt=current_time)
    
        return available_timeslots


class HospitalListView(generics.ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        review = serializer.save(patient=self.request.user)

        # Recalculate the doctor's average rating
        doctor_name = review.doctor_name
        reviews = doctor_name.reviews.all()
        total_reviews = reviews.count()
        total_rating = sum([review.rating for review in reviews])
        doctor_name.rating = total_rating / total_reviews
        doctor_name.num_reviews = total_reviews
        doctor_name.save()

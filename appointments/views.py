from django.shortcuts import render

# Create your views here.
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework import status, generics
from .models import PatientAppointment, UserMessages
from .serializers import PatientAppointmentSerializer,UserMessageSerializer
from django.utils import timezone
from pydoc import doc
from rest_framework.views import APIView
from doctors.models import TimeSlot

class PatientAppointmentCreateView(generics.CreateAPIView):
    queryset = PatientAppointment.objects.all()
    serializer_class = PatientAppointmentSerializer
    
    def perform_create(self, serializer):
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        appointment = serializer.save()
        print(appointment)

        subject = "Appointment Confirmation - HealthyCare Pvt. Ltd."
        recipient_email = appointment.patient.user.email
        from_email = "noreply@miltongaire.com"  # Must match your SendGrid sender

        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
                    <div style="text-align: center;">
                        <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" width="80" alt="Appointment Icon"/>
                        <h2 style="color: #2C3E50;">Appointment Confirmation</h2>
                    </div>
                    <p>Dear <strong>{appointment.patient.user.username}</strong>,</p>
                    <p>Your appointment has been successfully booked. Here are the details:</p>
                    <ul>
                        <li><strong>Department:</strong> {appointment.department_name}</li>
                        <li><strong>Doctor:</strong> {appointment.doctor.doctor_name}</li>
                 
                        <li><strong>Date:</strong> {appointment.timeslot.appointment_date}</li>
                        <li><strong>Time:</strong>{appointment.timeslot.start_time} - {appointment.timeslot.end_time}</li>
                    </ul>
                    <p>Thank you for choosing <strong>HealthyCare Pvt. Ltd.</strong>. If you have any questions, feel free to contact us.</p>
                    <p style="text-align: center; font-size: 14px; color: #666;">© 2025 HealthyCare Pvt. Ltd. All rights reserved.</p>
                </div>
            </body>
        </html>
        """

        # Create an email object
        email = EmailMultiAlternatives(subject, "", from_email, [recipient_email])
        email.attach_alternative(html_message, "text/html")  # Attach the HTML message
        email.send()

        return Response({"message": "Appointment booked, confirmation email sent"}, status=status.HTTP_201_CREATED)


class PatientAppointmentListView(generics.ListAPIView):
    serializer_class = PatientAppointmentSerializer
    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor')  # from ?doctor=Dr. Smith
        today = timezone.localdate()

        if doctor_id:
            return PatientAppointment.objects.filter(
                doctor=doctor_id,
                status__in=['scheduled','in-progress','completed']
            ).order_by('-booking_date')
        
        # Return none if doctor not provided to avoid exposing all new_appointments
        return PatientAppointment.objects.none()
    
class UpdatePatientAppointmentView(APIView):
    def put(self, request, appid, timeid):
        try:
            # Fetch the timeslot object first
            timeslot = TimeSlot.objects.get(id=timeid)
            
        except TimeSlot.DoesNotExist:
            return Response({"error": "TimeSlot not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            appointment = PatientAppointment.objects.get(timeslot=timeslot,patient__id=appid,)
        except PatientAppointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')

        if new_status not in dict(PatientAppointment.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # Update and save the status
        appointment.status = new_status
        appointment.save()

        return Response({"message": "Appointment status updated successfully"}, status=status.HTTP_200_OK)

        
        
            

            
    
    
    
class PatientAppointmentAllListView(generics.ListAPIView):
    serializer_class = PatientAppointmentSerializer
    
    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor')
        status=self.request.query_params.get('status').lower()
      
        
        qs = PatientAppointment.objects.filter(doctor_id=doctor_id)
        if doctor_id and status:
            filtered = qs.filter(status__iexact=status).order_by('-booking_date')
            return filtered
        return PatientAppointment.objects.none()
    

    
class UserMessagesCreateView(generics.CreateAPIView):
    queryset=UserMessages.objects.all()
    serializer_class = UserMessageSerializer
    
    def perform_create(self, serializer):
        message=serializer.save()
        
        subject = "Your Submission has been successfully received"
        recipient_email = message.email
        from_email= "noreply@miltongaire.com"
        
        
        html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
                               <div style="text-align: center;">
                        <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" width="80" alt="Appointment Icon"/>
                        <h2 style="color: #2C3E50;">Submission Successful</h2>
                    </div>
                <p>Dear <strong>{message.fullname}</strong>,</p>
                <p>We have received your message. Thank you for reaching out to us! Our team will get back to you as soon as possible.</p>
                <p>If your query is urgent, you may contact us directly at <a href="mailto:support@healthycare.com">support@healthycare.com</a>.</p>
                                   <p style="text-align: center; font-size: 14px; color: #666;">© 2025 HealthyCare Pvt. Ltd. All rights reserved.</p>
            </div>
        </body>
    </html>
"""



               
        email = EmailMultiAlternatives(subject, "", from_email, [recipient_email])
        email.attach_alternative(html_message, "text/html")  # Attach the HTML message
        email.send()

        return Response({"message": "Message Received, confirmation email sent"}, status=status.HTTP_201_CREATED) 
    
    
    
    
    

    
        
    
    
    

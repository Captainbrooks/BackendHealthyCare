from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer
from .models import User, PasswordResetToken

from django.utils import timezone
from datetime import timedelta
from authentication.utils import generate_verification_code, \
    send_verification_email, generate_forgotpassword_link, send_password_reset_email,passwordChangeSuccessEmail
from authentication.serializers import ForgotPasswordRequestSerializer, \
    ResetPasswordSerializer
from smtplib import SMTPException
from django.http.response import BadHeaderError
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated

from doctors.models import Doctors
from rest_framework_simplejwt.authentication import JWTAuthentication



from .serializers import *
from rest_framework.decorators import permission_classes


class RegisterView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response({
                "message": "User registered successfully",
                "access_token": result['access'],
                "refresh_token": result['refresh'],
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error":
            serializer.errors, "status":status.HTTP_400_BAD_REQUEST
            })
    
    
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            
            return Response({
                'access_token': serializer.validated_data['access'],  # Correct key
                'refresh_token': serializer.validated_data['refresh'],
            }, status=status.HTTP_200_OK)

        print("Serializer Errors:", serializer.errors)
        return Response({
            'error': serializer.errors.get('non_field_errors', ['Something went wrong. Please try again later.'])[0]
        }, status=status.HTTP_401_UNAUTHORIZED)
        
        
class VerifyCodeView(APIView):

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        print("verify code is reached")
        
        print("email", email)
        print("from user code", code)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"Invalid Email"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_verified:
            return Response({"message": "Already verified."}, status=status.HTTP_200_OK)
        
        if user.verification_code != code:
            return Response({"error":"Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > user.code_generated_at + timedelta(minutes=10):
            return Response({"error":"Verification code expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = True
        user.is_verified = True
        user.verification_code = None
        user.code_generated_at = None
        
        user.save()
        
        return Response({
            "message":"Email verified successfully"
        })
        
        
class ResendVerificationCodeView(APIView):

    def post(self, request):
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_verified:
            return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)
        
        code = generate_verification_code()
        print(code)
        user.verification_code = code
        user.code_generated_at = timezone.now()
        user.save()
        
        send_verification_email(email, code) 
        return Response({"message": "Verification code resent."}, status=status.HTTP_200_OK)      
    
    
class ForgotPasswordView(APIView):

    def post(self, request):
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)
        
        try:
            reset_token = generate_forgotpassword_link(user)
        
            send_password_reset_email(user.email, reset_token.token)
        except (SMTPException, BadHeaderError, Exception) as e:
            return Response({
                "error":'Something went wrong while sending the reset link.Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({
            "message":f"Password reset link has been sent to {email}"
        }, status=status.HTTP_200_OK)

        
class ResetPasswordView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]
        
        try:
            token_obj = PasswordResetToken.objects.get(token=token) 
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Invalid or tampered token."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not token_obj.is_valid():
            return Response({"error": "Token expired or already used."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = token_obj.user
        user.set_password(new_password)
        user.save()
        
        token_obj.used = True
        token_obj.save()
        
        logout(request)
        
        passwordChangeSuccessEmail(user.email)
        
        return Response({"message": "Password has been reset successfully. Redirecting to login page."}, status=status.HTTP_200_OK)
    
    
    
    
class DoctorDashBoardAccessCheck(APIView):
    def post(self, request):
        email = request.data.get('email')
        role = request.data.get('role')

        if role != 'Doctor':
            return Response({"detail": "Access denied. Not a doctor."}, status=status.HTTP_403_FORBIDDEN)

        if not Doctors.objects.filter(user__email=email).exists():
            return Response({"detail": "Doctor profile not found."}, status=status.HTTP_403_FORBIDDEN)

        return Response({"allowed": True})
        
        
            
        
        
        


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .utils import generate_verification_code, send_verification_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.utils import timezone
from datetime import timedelta
from doctors.models import Doctors
from patients.models import Patient

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
        
    def create(self, validated_data):
        
        code = generate_verification_code()
        print("Code", code)
        now = timezone.now()
            
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
            verification_code=code,
            code_generated_at=now
            
        )
        
        
        print(user)
        Patient.objects.create(
            user=user,
            full_name=validated_data['username']
        )
        
        send_verification_email(user.email, code)
        
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        
        if Doctors.objects.filter(user=user).exists():
            doctor = Doctors.objects.get(user=user)
            refresh['role'] = 'Doctor'
            refresh['id'] = doctor.id
        else:
            patient = Patient.objects.get(user=user)
            print("patient",patient.id)
            refresh['role'] = 'Patient'
            refresh['id'] = patient.id
        
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return {
            'user': user,
            'access': access_token,
            'refresh': refresh_token
        }
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
            print("user",user)
            print("active", user.is_verified)
            
            
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found with this email.")
        
        if not user.is_verified:
            raise serializers.ValidationError("User email is not verified. Please verify your email before logging in.")

        user = authenticate(email=email, password=password)
        
        
        if user is None:
            raise serializers.ValidationError("Incorrect password.")
        
                # Generate JWT token
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        refresh['email']=user.email
        
        
        
        
        
        
        
        
        if Doctors.objects.filter(user=user).exists():
            doctor=Doctors.objects.get(user=user)
            
            print("User", doctor)
           
            
            refresh['role'] = 'Doctor'
            refresh['id']=doctor.id
            
        else:
            patient, created = Patient.objects.get_or_create(user=user)
            print("patient",patient.id)
            refresh['role'] = 'Patient'
            refresh['id'] = patient.id
            
            
            
            



        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    
    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data=super().validate(attrs)
        data['role']-self.user.role
        return data
        
        
    

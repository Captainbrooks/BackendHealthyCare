from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

import secrets

def generate_reset_token():
    return secrets.token_urlsafe(32)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)
    
    

class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES=(
        ('doctor','Doctor'),
        ('patient', 'Patient'),
        
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    verification_code=models.CharField(max_length=6,blank=True, null=True)
    code_generated_at = models.DateTimeField(blank=True, null=True)
    
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Specify related_name to avoid conflicts with default User model fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    
    
class PasswordResetToken(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=128,unique=True,default=generate_reset_token)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()
    used=models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.used and self.expires_at > timezone.now()
    
    def __str__(self):
        return f"Reset token for {self.user.email}"
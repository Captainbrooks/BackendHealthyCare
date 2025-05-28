import os
import random
from django.core.mail import EmailMultiAlternatives
import secrets
from datetime import timedelta
from django.utils import timezone
from authentication.models import PasswordResetToken
import hashlib


def generate_verification_code():
    return str(random.randint(100000, 999999))





def send_verification_email(email, code):
    subject = "Verify your email"
    recipient_email=email
    from_email = "noreply@miltongaire.com"
    
    
    html_message = f"""
    <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
            <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" width="80" alt="Appointment Icon" />
            <h2 style="color: #2C3E50; margin: 0;">Email Verification</h2>
            </div>
      
            <p style="font-size: 16px; color: #34495e;">Your verification code is: <span style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">{code}<span></p>
           
            <p style="font-size: 16px; color: #34495e; text-align:center">It will expire in 10 minutes.</p>
      
            <div style="margin-top: 20px; text-align: center;">
            <p style="font-size: 14px; color: #7f8c8d;">If you did not request this, please ignore this message.</p>
            </div>

            <p style="text-align: center; font-size: 14px; color: #666; margin-top: 20px;">© 2025 HealthyCare Pvt. Ltd. All rights reserved.</p>
            </div>
            </body>
    </html>
        """

        # Create an email object
    verification_email = EmailMultiAlternatives(subject, "", from_email, [recipient_email])
    verification_email.attach_alternative(html_message, "text/html")  # Attach the HTML message
    verification_email.send()
    
    
    
def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()
    
def generate_reset_token():
    raw_token = secrets.token_urlsafe(32)
    print("raw_token", raw_token)
    hashed=hash_token(raw_token)
    print("hashed token", hashed)
    
    
    return hashed
    
def generate_forgotpassword_link(user):
    resettoken=generate_reset_token()
    
    expiration_time=timezone.now() + timedelta(minutes=30)
    
    forgotpasswordtoken=PasswordResetToken.objects.create(
        user=user,
        token=resettoken,
        expires_at=expiration_time   
    )
    
    return forgotpasswordtoken





def send_password_reset_email(email, token):
    reset=os.getenv('FRONTEND_URL')
    reset_url = f"{reset}/reset-password/{token}"
    subject = "Reset Your Password"
    recipient_email = email
    from_email = "noreply@miltongaire.com"

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
        <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" width="80" alt="Reset Password Icon" />
        <h2 style="color: #2C3E50; margin: 0;">Reset Your Password</h2>
        </div>

        <p style="font-size: 16px; color: #34495e;">Click the button below to reset your password:</p>
        
        <div style="text-align: center; margin: 20px 0;">
            <a href="{reset_url}" style="display: inline-block; padding: 12px 24px; font-size: 16px; font-weight: bold; color: #fff; background-color: #27ae60; text-decoration: none; border-radius: 6px;">Reset Password</a>
        </div>

        <p style="font-size: 16px; color: #34495e; text-align:center">This link will expire in 30 minutes.</p>

        <div style="margin-top: 20px; text-align: center;">
        <p style="font-size: 14px; color: #7f8c8d;">If you did not request this, please ignore this message.</p>
        </div>

        <p style="text-align: center; font-size: 14px; color: #666; margin-top: 20px;">© 2025 HealthyCare Pvt. Ltd. All rights reserved.</p>
        </div>
        </body>
    </html>
    """

    reset_email = EmailMultiAlternatives(subject, "", from_email, [recipient_email])
    reset_email.attach_alternative(html_message, "text/html")
    reset_email.send()
    
    
    
    
    
    
def passwordChangeSuccessEmail(email):
    subject = "Your Password Has Been Changed"
    recipient_email = email
    from_email = "noreply@miltongaire.com"

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
        <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://cdn-icons-png.flaticon.com/512/190/190411.png" width="80" alt="Password Changed Icon" />
        <h2 style="color: #2C3E50; margin: 0;">Password Successfully Changed</h2>
        </div>

        <p style="font-size: 16px; color: #34495e;">Your password has been changed successfully.</p>
        
        <p style="font-size: 16px; color: #34495e;">If you did not perform this change, please contact support immediately.</p>

        <div style="margin-top: 20px; text-align: center;">
        <p style="font-size: 14px; color: #7f8c8d;">If you made this change, no further action is required.</p>
        </div>

        <p style="text-align: center; font-size: 14px; color: #666; margin-top: 20px;">© 2025 HealthyCare Pvt. Ltd. All rights reserved.</p>
        </div>
        </body>
    </html>
    """

    email_message = EmailMultiAlternatives(subject, "", from_email, [recipient_email])
    email_message.attach_alternative(html_message, "text/html")
    email_message.send()
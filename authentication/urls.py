from django.urls import path
from .views import RegisterView, LoginView, VerifyCodeView, ResendVerificationCodeView, ForgotPasswordView, ResetPasswordView,DoctorDashBoardAccessCheck

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("verify-code/", VerifyCodeView.as_view(), name="verify-code"),
    path("resend-code/", ResendVerificationCodeView.as_view(), name="resend-code"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('dashboard-access-check/',DoctorDashBoardAccessCheck.as_view(),name='access_check')
    
]

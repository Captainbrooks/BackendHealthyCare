from django.urls import path
from . import views
from .views import PatientAppointmentCreateView,PatientAppointmentListView

urlpatterns = [
    path('list/', views.PatientAppointmentListView.as_view(), name='appointment-list'),
    path('all/',views.PatientAppointmentAllListView.as_view(),name='all_appointment_based_on_doctor'),
    path('create/', views.PatientAppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:id>/status/',views.UpdatePatientAppointmentView.as_view(),name='update-status'),
    path('message/',views.UserMessagesCreateView.as_view(),name="user_message")
]

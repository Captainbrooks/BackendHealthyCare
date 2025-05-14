
from django.urls import path
from patients.views import *

urlpatterns = [
   path('<int:id>/', PatientView.as_view(), name='patient-history'),
   path('add-test-results/<int:id>/', TestResultCreateView.as_view(),name="add-test-results"),
   path('delete-test-results/<int:patientId>/<int:test_id>', TestResultDeleteView.as_view(),name="delete-test-results"),
   path('add-vital-signs/<int:patientId>/',VitalSignsCreateView.as_view(),name='add-vital-signs'),
   path('delete-vital-signs/<int:patientId>/<int:vital_id>', VitalSignDeleteView.as_view(),name="delete-vital-signs"),
   path('add-medication/<int:patientId>/',MedicationCreateView.as_view(),name='add-medication'),
   path('delete-medication/<int:patientId>/<int:medication_id>/',MedicationDeleteView.as_view(),name='delete-medication'),
   path('update-medication/<int:patientId>/<int:medication_id>/', UpdateMedicationView.as_view(),name='update-medication'),
    
]

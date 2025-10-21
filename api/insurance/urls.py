from django.urls import path
from .views import predict_insurance, get_insurance_data

urlpatterns = [
    path('predict/', predict_insurance),
    path('data/', get_insurance_data),
]

from django.urls import path
from .views import predict_diabetes, diabetes_roc_data

urlpatterns = [
    path('predict/', predict_diabetes),
    path('roc-data/', diabetes_roc_data),  # 👈 nuevo endpoint
]

from django.urls import path
from .views import corregir

urlpatterns = [
    path('corregir/', corregir, name='corregir'),
]

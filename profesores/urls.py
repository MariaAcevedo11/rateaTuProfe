# profesores/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.registro_usuario, name='registro_usuario'),  # o cualquier vista principal
]

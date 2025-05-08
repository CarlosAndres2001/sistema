from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.usuarios, name='usuarios_usuario'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('crear_rol/', views.crear_rol, name='crear_rol'),
]


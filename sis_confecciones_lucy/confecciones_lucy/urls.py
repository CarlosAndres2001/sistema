"""
URL configuration for confecciones_lucy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import views as auth_views 
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'), 
    path('base/', views.base_view, name='base'),  
    path('ventas/', include('ventas.urls')),  
    path('compras/', include('compras.urls')),  
    path('produccion/', include('produccion.urls')), 
    path('usuarios/', include('usuarios.urls')),  
]


   

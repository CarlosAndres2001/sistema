from django.urls import path
from . import views

urlpatterns = [
    path('crear_insumo', views.crear_insumo, name='crear_insumo'),
    path('crear_depositos', views.crear_depositos, name='crear_depositos'),
    path('crear_proveedor', views.crear_proveedor, name='crear_proveedor'),
    path('solicitud_compra/', views.solicitud_compra, name='solicitud_compra'),
    path('registrar_compra/', views.registrar_compra, name='registrar_compra'),
    path('registrar_compraa/', views.registrar_compraa, name='registrar_compraa'),
]



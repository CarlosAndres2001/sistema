from django.urls import path
from . import views

urlpatterns = [
    path('clientes/',views.clientes, name='ventas_clientes'),
    path('pago/',views.pagos, name='ventas_pago'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('ventaa',views.ventaa, name='ventaa'),
    path('registrar_venta',views.registrar_venta, name='registrar_venta'),
    path('ticket/<int:venta_id>/', views.ticket_venta, name='ticket_venta'),
    path('lista_ventas', views.lista_ventas, name='lista_ventas'),
]



from django.urls import path
from . import views

urlpatterns = [

    path('gestionar_categorias', views.gestionar_categorias, name='gestionar_categorias'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear-subcategoria/', views.crear_subcategoria, name='crear_subcategoria'),
    path('listar_categorias', views.listar_categorias, name="listar_categorias"),
    path('crear_producto', views.crear_producto, name='crear_producto')
]


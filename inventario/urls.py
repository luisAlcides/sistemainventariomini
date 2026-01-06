from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.lista_productos, name='productos'),
    path('productos/por-agotarse/', views.productos_por_agotarse, name='productos_por_agotarse'),
    path('entradas/', views.lista_entradas, name='entradas'),
    path('entradas/nueva/', views.nueva_entrada, name='entrada_nueva'),
    path('ajustes/', views.lista_ajustes, name='ajustes'),
]


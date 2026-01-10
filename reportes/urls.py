from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.index, name='index'),
    # Reportes de Ventas
    path('ventas-dia/', views.ventas_dia, name='ventas_dia'),
    path('ventas-rango/', views.ventas_rango, name='ventas_rango'),
    # Reportes de Productos
    path('productos-por-agotarse/', views.productos_por_agotarse, name='productos_por_agotarse'),
    path('productos-mas-vendidos/', views.productos_mas_vendidos, name='productos_mas_vendidos'),
    path('valor-inventario/', views.valor_inventario, name='valor_inventario'),
    # Reportes de Clientes
    path('clientes-frecuentes/', views.clientes_frecuentes, name='clientes_frecuentes'),
]


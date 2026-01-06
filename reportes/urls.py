from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.index, name='index'),
    path('ventas-dia/', views.ventas_dia, name='ventas_dia'),
    path('productos-por-agotarse/', views.productos_por_agotarse, name='productos_por_agotarse'),
]


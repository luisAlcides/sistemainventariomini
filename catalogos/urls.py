from django.urls import path
from . import views

app_name = 'catalogos'

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.lista_productos, name='productos'),
    path('productos/nuevo/', views.producto_nuevo, name='producto_nuevo'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('categorias/', views.lista_categorias, name='categorias'),
]


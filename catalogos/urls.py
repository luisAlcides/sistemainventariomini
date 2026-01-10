from django.urls import path
from . import views

app_name = 'catalogos'

urlpatterns = [
    path('', views.index, name='index'),
    # Productos
    path('productos/', views.lista_productos, name='productos'),
    path('productos/nuevo/', views.producto_nuevo, name='producto_nuevo'),
    path('productos/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('productos/<int:producto_id>/editar/', views.producto_editar, name='producto_editar'),
    # Clientes
    path('clientes/', views.lista_clientes, name='clientes'),
    path('clientes/nuevo/', views.cliente_nuevo, name='cliente_nuevo'),
    path('clientes/<int:cliente_id>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:cliente_id>/editar/', views.cliente_editar, name='cliente_editar'),
    # Categorías
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/nueva/', views.categoria_nueva, name='categoria_nueva'),
    path('categorias/<int:categoria_id>/editar/', views.categoria_editar, name='categoria_editar'),
    # Nombres de Productos
    path('nombres-productos/', views.lista_nombres_productos, name='nombres_productos'),
    path('nombres-productos/nuevo/', views.nombre_producto_nuevo, name='nombre_producto_nuevo'),
    path('nombres-productos/<int:nombre_producto_id>/', views.nombre_producto_detalle, name='nombre_producto_detalle'),
    path('nombres-productos/<int:nombre_producto_id>/editar/', views.nombre_producto_editar, name='nombre_producto_editar'),
]


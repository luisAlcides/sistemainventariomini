from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.lista_productos, name='productos'),
    path('productos/nuevo/', views.crear_producto, name='producto_nuevo'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/por-agotarse/', views.productos_por_agotarse, name='productos_por_agotarse'),
    path('entradas/', views.lista_entradas, name='entradas'),
    path('entradas/nueva/', views.nueva_entrada, name='entrada_nueva'),
    path('entradas/<int:entrada_id>/', views.detalle_entrada, name='detalle_entrada'),
    path('ajustes/', views.lista_ajustes, name='ajustes'),
    path('ajustes/nuevo/', views.crear_ajuste, name='ajuste_nuevo'),
    path('api/producto/<int:producto_id>/', views.obtener_producto_info, name='obtener_producto_info'),
]


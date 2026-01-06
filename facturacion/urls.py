from django.urls import path
from . import views

app_name = 'facturacion'

urlpatterns = [
    path('', views.index, name='index'),
    path('nueva/', views.nueva_factura, name='nueva'),
    path('<int:factura_id>/', views.detalle_factura, name='detalle'),
]


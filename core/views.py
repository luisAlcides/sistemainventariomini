"""
Vistas principales del sistema.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q, F
from datetime import date

from ventas.models import Factura, Cliente
from inventario.models import Producto


@login_required
def dashboard(request):
    """
    Vista del dashboard principal con resumen del sistema.
    """
    fecha_actual = timezone.now()
    hoy = date.today()
    
    # Ventas del día
    ventas_dia = Factura.objects.filter(
        fecha_venta__date=hoy,
        estado='COMPLETADA'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Productos por agotarse (usando F para comparar campos)
    productos_por_agotarse = Producto.objects.filter(
        activo=True
    ).filter(
        stock_actual__lte=F('stock_minimo')
    ).count()
    
    # Total de productos activos
    total_productos = Producto.objects.filter(activo=True).count()
    
    # Total de clientes activos
    total_clientes = Cliente.objects.filter(activo=True).count()
    
    # Últimas 5 facturas
    ultimas_facturas = Factura.objects.filter(
        estado='COMPLETADA'
    ).order_by('-fecha_venta')[:5]
    
    context = {
        'fecha_actual': fecha_actual,
        'ventas_dia': ventas_dia,
        'productos_por_agotarse': productos_por_agotarse,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'ultimas_facturas': ultimas_facturas,
    }
    
    return render(request, 'dashboard.html', context)


"""
Vistas para el módulo de reportes.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import date, timedelta

from ventas.models import Factura, DetalleFactura
from inventario.models import Producto


@login_required
def index(request):
    """
    Índice de reportes.
    """
    return render(request, 'reportes/index.html')


@login_required
def ventas_dia(request):
    """
    Reporte de ventas del día.
    """
    hoy = date.today()
    
    facturas = Factura.objects.filter(
        fecha_venta__date=hoy,
        estado='COMPLETADA'
    ).order_by('-fecha_venta')
    
    total_ventas = facturas.aggregate(total=Sum('total'))['total'] or 0
    cantidad_facturas = facturas.count()
    
    context = {
        'fecha': hoy,
        'facturas': facturas,
        'total_ventas': total_ventas,
        'cantidad_facturas': cantidad_facturas,
    }
    
    return render(request, 'reportes/ventas_dia.html', context)


@login_required
def productos_por_agotarse(request):
    """
    Reporte de productos por agotarse.
    """
    from django.db.models import F
    
    productos = Producto.objects.filter(
        activo=True
    ).filter(
        stock_actual__lte=F('stock_minimo')
    ).order_by('stock_actual')
    
    context = {
        'productos': productos,
    }
    
    return render(request, 'reportes/productos_por_agotarse.html', context)


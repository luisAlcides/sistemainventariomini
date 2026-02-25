"""
Vistas principales del sistema.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q, F
from datetime import date, timedelta
from decimal import Decimal
from collections import defaultdict

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

    # Productos por expirar (próximos 30 días)
    fecha_limite = hoy + timedelta(days=30)
    productos_por_expirar = Producto.objects.filter(
        activo=True,
        fecha_expiracion__lte=fecha_limite
    ).count()
    
    # Últimas 5 facturas
    ultimas_facturas = Factura.objects.filter(
        estado='COMPLETADA'
    ).order_by('-fecha_venta')[:5]

    # Tendencia de ventas (últimas 8 semanas, regresión lineal)
    inicio_tendencia = hoy - timedelta(days=7 * 8)
    facturas_tendencia = Factura.objects.filter(
        fecha_venta__date__gte=inicio_tendencia,
        fecha_venta__date__lte=hoy,
        estado='COMPLETADA',
    )
    por_semana = defaultdict(Decimal)
    for f in facturas_tendencia:
        delta = (f.fecha_venta.date() - inicio_tendencia).days
        num_semana = delta // 7
        por_semana[num_semana] += f.total
    semanas_orden = sorted(por_semana.keys())
    if len(semanas_orden) >= 2:
        n = len(semanas_orden)
        x = semanas_orden
        y = [float(por_semana[k]) for k in x]
        sum_x, sum_y = sum(x), sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        denom = n * sum_x2 - sum_x * sum_x
        pendiente = (n * sum_xy - sum_x * sum_y) / denom if denom != 0 else 0
        promedio_y = sum_y / n
        umbral = promedio_y * 0.05 if promedio_y else 100
        if pendiente > umbral:
            tendencia_ventas = 'alcista'
        elif pendiente < -umbral:
            tendencia_ventas = 'bajista'
        else:
            tendencia_ventas = 'estable'
    else:
        tendencia_ventas = 'estable'
    
    context = {
        'fecha_actual': fecha_actual,
        'ventas_dia': ventas_dia,
        'productos_por_agotarse': productos_por_agotarse,
        'productos_por_expirar': productos_por_expirar,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'ultimas_facturas': ultimas_facturas,
        'tendencia_ventas': tendencia_ventas,
    }
    
    return render(request, 'dashboard.html', context)


"""
Vistas para el módulo de reportes.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, F, Avg, Max, Min
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from ventas.models import Factura, DetalleFactura, Cliente
from inventario.models import Producto, Categoria
from usuarios.models import Usuario
from .forms import RangoFechasForm, ReporteVentasForm


@login_required
def index(request):
    """
    Índice de reportes con resumen general.
    """
    hoy = date.today()
    mes_actual = hoy.replace(day=1)
    
    # Estadísticas del día
    ventas_hoy = Factura.objects.filter(
        fecha_venta__date=hoy,
        estado='COMPLETADA'
    )
    total_ventas_hoy = ventas_hoy.aggregate(total=Sum('total'))['total'] or 0
    cantidad_facturas_hoy = ventas_hoy.count()
    
    # Estadísticas del mes
    ventas_mes = Factura.objects.filter(
        fecha_venta__date__gte=mes_actual,
        estado='COMPLETADA'
    )
    total_ventas_mes = ventas_mes.aggregate(total=Sum('total'))['total'] or 0
    cantidad_facturas_mes = ventas_mes.count()
    
    # Productos por agotarse
    productos_por_agotarse = Producto.objects.filter(
        activo=True,
        stock_actual__lte=F('stock_minimo')
    ).count()
    
    # Valor total del inventario
    valor_inventario = Producto.objects.filter(
        activo=True
    ).aggregate(
        total=Sum(F('stock_actual') * F('precio_compra'))
    )['total'] or 0
    
    context = {
        'total_ventas_hoy': total_ventas_hoy,
        'cantidad_facturas_hoy': cantidad_facturas_hoy,
        'total_ventas_mes': total_ventas_mes,
        'cantidad_facturas_mes': cantidad_facturas_mes,
        'productos_por_agotarse': productos_por_agotarse,
        'valor_inventario': valor_inventario,
    }
    
    return render(request, 'reportes/index.html', context)


@login_required
def ventas_dia(request):
    """
    Reporte de ventas del día.
    """
    fecha_seleccionada = request.GET.get('fecha', str(date.today()))
    try:
        fecha = date.fromisoformat(fecha_seleccionada)
    except (ValueError, TypeError):
        fecha = date.today()
    
    facturas = Factura.objects.filter(
        fecha_venta__date=fecha,
        estado='COMPLETADA'
    ).order_by('-fecha_venta')
    
    total_ventas = facturas.aggregate(total=Sum('total'))['total'] or 0
    cantidad_facturas = facturas.count()
    promedio_venta = total_ventas / cantidad_facturas if cantidad_facturas > 0 else 0
    
    # Ventas por hora (simplificado para compatibilidad)
    ventas_por_hora = []
    horas_dict = {}
    for factura in facturas:
        hora = factura.fecha_venta.hour
        if hora not in horas_dict:
            horas_dict[hora] = {'total': 0, 'cantidad': 0}
        horas_dict[hora]['total'] += float(factura.total)
        horas_dict[hora]['cantidad'] += 1
    
    ventas_por_hora = [{'hora': h, 'total': v['total'], 'cantidad': v['cantidad']} 
                       for h, v in sorted(horas_dict.items())]
    
    context = {
        'fecha': fecha,
        'facturas': facturas,
        'total_ventas': total_ventas,
        'cantidad_facturas': cantidad_facturas,
        'promedio_venta': promedio_venta,
        'ventas_por_hora': ventas_por_hora,
    }
    
    return render(request, 'reportes/ventas_dia.html', context)


@login_required
def ventas_rango(request):
    """
    Reporte de ventas por rango de fechas.
    """
    form = ReporteVentasForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        vendedor_id = form.cleaned_data.get('vendedor')
        
        facturas = Factura.objects.filter(
            fecha_venta__date__gte=fecha_inicio,
            fecha_venta__date__lte=fecha_fin,
            estado='COMPLETADA'
        )
        
        if vendedor_id:
            facturas = facturas.filter(vendedor_id=vendedor_id)
        
        facturas = facturas.order_by('-fecha_venta')
        
        # Estadísticas
        total_ventas = facturas.aggregate(total=Sum('total'))['total'] or 0
        cantidad_facturas = facturas.count()
        promedio_venta = total_ventas / cantidad_facturas if cantidad_facturas > 0 else 0
        total_descuentos = facturas.aggregate(total=Sum('descuento'))['total'] or 0
        
        # Ventas por día (simplificado para compatibilidad)
        ventas_por_dia = []
        dias_dict = {}
        for factura in facturas:
            dia = factura.fecha_venta.date()
            if dia not in dias_dict:
                dias_dict[dia] = {'total': 0, 'cantidad': 0}
            dias_dict[dia]['total'] += float(factura.total)
            dias_dict[dia]['cantidad'] += 1
        
        ventas_por_dia = [{'dia': d, 'total': v['total'], 'cantidad': v['cantidad']} 
                          for d, v in sorted(dias_dict.items())]
        
        # Top vendedores
        top_vendedores = facturas.values(
            'vendedor__first_name',
            'vendedor__last_name',
            'vendedor__username'
        ).annotate(
            total=Sum('total'),
            cantidad=Count('id')
        ).order_by('-total')[:10]
        
        context = {
            'form': form,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'facturas': facturas[:100],  # Limitar a 100 para no sobrecargar
            'total_ventas': total_ventas,
            'cantidad_facturas': cantidad_facturas,
            'promedio_venta': promedio_venta,
            'total_descuentos': total_descuentos,
            'ventas_por_dia': ventas_por_dia,
            'top_vendedores': top_vendedores,
        }
    else:
        # Valores por defecto
        hoy = date.today()
        fecha_inicio = hoy - timedelta(days=30)
        fecha_fin = hoy
        
        facturas = Factura.objects.filter(
            fecha_venta__date__gte=fecha_inicio,
            fecha_venta__date__lte=fecha_fin,
            estado='COMPLETADA'
        ).order_by('-fecha_venta')
        
        total_ventas = facturas.aggregate(total=Sum('total'))['total'] or 0
        cantidad_facturas = facturas.count()
        
        context = {
            'form': form,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'facturas': facturas[:100],
            'total_ventas': total_ventas,
            'cantidad_facturas': cantidad_facturas,
        }
    
    return render(request, 'reportes/ventas_rango.html', context)


@login_required
def productos_por_agotarse(request):
    """
    Reporte de productos por agotarse.
    """
    productos = Producto.objects.filter(
        activo=True,
        stock_actual__lte=F('stock_minimo')
    ).order_by('stock_actual')
    
    # Estadísticas
    total_productos = productos.count()
    valor_total = sum(p.calcular_valor_inventario() for p in productos)
    
    context = {
        'productos': productos,
        'total_productos': total_productos,
        'valor_total': valor_total,
    }
    
    return render(request, 'reportes/productos_por_agotarse.html', context)


@login_required
def productos_mas_vendidos(request):
    """
    Reporte de productos más vendidos.
    """
    form = RangoFechasForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
    else:
        hoy = date.today()
        fecha_inicio = hoy - timedelta(days=30)
        fecha_fin = hoy
    
    # Productos más vendidos en el rango de fechas
    productos_vendidos = DetalleFactura.objects.filter(
        factura__fecha_venta__date__gte=fecha_inicio,
        factura__fecha_venta__date__lte=fecha_fin,
        factura__estado='COMPLETADA'
    ).values(
        'producto__id',
        'producto__nombre',
        'producto__codigo',
        'producto__categoria__nombre'
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        total_ventas=Sum('subtotal'),
        veces_vendido=Count('id')
    ).order_by('-cantidad_vendida')[:20]
    
    context = {
        'form': form,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'productos_vendidos': productos_vendidos,
    }
    
    return render(request, 'reportes/productos_mas_vendidos.html', context)


@login_required
def valor_inventario(request):
    """
    Reporte de valor de inventario.
    """
    # Por categoría
    valor_por_categoria = Producto.objects.filter(
        activo=True
    ).values(
        'categoria__nombre'
    ).annotate(
        cantidad_productos=Count('id'),
        valor_total=Sum(F('stock_actual') * F('precio_compra'))
    ).order_by('-valor_total')
    
    # Total general
    productos = Producto.objects.filter(activo=True)
    valor_total = sum(p.calcular_valor_inventario() for p in productos)
    cantidad_total = productos.count()
    
    # Productos de mayor valor
    productos_valor = productos.annotate(
        valor=F('stock_actual') * F('precio_compra')
    ).order_by('-valor')[:20]
    
    context = {
        'valor_por_categoria': valor_por_categoria,
        'valor_total': valor_total,
        'cantidad_total': cantidad_total,
        'productos_valor': productos_valor,
    }
    
    return render(request, 'reportes/valor_inventario.html', context)


@login_required
def clientes_frecuentes(request):
    """
    Reporte de clientes más frecuentes.
    """
    form = RangoFechasForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
    else:
        hoy = date.today()
        fecha_inicio = hoy - timedelta(days=30)
        fecha_fin = hoy
    
    # Clientes más frecuentes
    clientes_frecuentes = Factura.objects.filter(
        fecha_venta__date__gte=fecha_inicio,
        fecha_venta__date__lte=fecha_fin,
        estado='COMPLETADA',
        cliente__isnull=False
    ).values(
        'cliente__id',
        'cliente__nombre',
        'cliente__tipo_cliente'
    ).annotate(
        total_compras=Sum('total'),
        cantidad_facturas=Count('id'),
        promedio_compra=Avg('total')
    ).order_by('-total_compras')[:20]
    
    context = {
        'form': form,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'clientes_frecuentes': clientes_frecuentes,
    }
    
    return render(request, 'reportes/clientes_frecuentes.html', context)


"""
Vistas para el módulo de facturación.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone

from ventas.models import Factura, DetalleFactura, Cliente
from ventas.utils import generar_numero_factura
from inventario.models import Producto


@login_required
def index(request):
    """
    Lista de facturas.
    """
    facturas = Factura.objects.all().order_by('-fecha_venta')[:50]
    
    # Filtros
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    
    if query:
        facturas = facturas.filter(
            Q(numero_factura__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente_nombre__icontains=query)
        )
    
    if estado:
        facturas = facturas.filter(estado=estado)
    
    context = {
        'facturas': facturas,
        'query': query,
        'estado_selected': estado,
    }
    
    return render(request, 'facturacion/index.html', context)


@login_required
def nueva_factura(request):
    """
    Crear una nueva factura.
    """
    if request.method == 'POST':
        # Lógica para crear factura (se implementará con formularios)
        messages.success(request, 'Factura creada exitosamente')
        return redirect('facturacion:index')
    
    # Obtener productos disponibles
    productos = Producto.objects.filter(activo=True, stock_actual__gt=0)
    clientes = Cliente.objects.filter(activo=True)
    
    context = {
        'productos': productos,
        'clientes': clientes,
        'numero_factura': generar_numero_factura(),
    }
    
    return render(request, 'facturacion/nueva.html', context)


@login_required
def detalle_factura(request, factura_id):
    """
    Ver detalle de una factura.
    """
    factura = get_object_or_404(Factura, id=factura_id)
    detalles = factura.detalles.all()
    
    context = {
        'factura': factura,
        'detalles': detalles,
    }
    
    return render(request, 'facturacion/detalle.html', context)


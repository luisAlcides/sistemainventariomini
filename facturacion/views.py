"""
Vistas para el módulo de facturación.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from decimal import Decimal
import json

from ventas.models import Factura, DetalleFactura, Cliente
from ventas.utils import generar_numero_factura
from inventario.models import Producto
from .forms import FacturaForm


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
    Crear una nueva factura con múltiples productos.
    """
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            cliente_id = request.POST.get('cliente', '')
            cliente_nombre = request.POST.get('cliente_nombre', '').strip()
            descuento = Decimal(request.POST.get('descuento', 0) or 0)
            observaciones = request.POST.get('observaciones', '').strip()
            
            # Obtener productos del JSON
            productos_json = request.POST.get('productos', '[]')
            productos_data = json.loads(productos_json)
            
            if not productos_data:
                messages.error(request, 'Debe agregar al menos un producto a la factura.')
                return redirect('facturacion:nueva')
            
            # Validar stock antes de crear la factura
            productos_invalidos = []
            for item in productos_data:
                producto_id = item.get('producto_id')
                cantidad = int(item.get('cantidad', 0))
                
                try:
                    producto = Producto.objects.get(id=producto_id, activo=True)
                    if cantidad > producto.stock_actual:
                        productos_invalidos.append({
                            'producto': producto.nombre,
                            'disponible': producto.stock_actual,
                            'solicitado': cantidad
                        })
                except Producto.DoesNotExist:
                    productos_invalidos.append({
                        'producto': f'ID {producto_id}',
                        'disponible': 0,
                        'solicitado': cantidad
                    })
            
            if productos_invalidos:
                error_msg = 'Stock insuficiente para los siguientes productos:\n'
                for item in productos_invalidos:
                    error_msg += f"- {item['producto']}: Disponible {item['disponible']}, Solicitado {item['solicitado']}\n"
                messages.error(request, error_msg)
                return redirect('facturacion:nueva')
            
            # Crear factura con transacción
            with transaction.atomic():
                # Crear la factura
                factura = Factura.objects.create(
                    numero_factura=generar_numero_factura(),
                    cliente_id=int(cliente_id) if cliente_id else None,
                    cliente_nombre=cliente_nombre if not cliente_id else None,
                    vendedor=request.user,
                    descuento=descuento,
                    observaciones=observaciones,
                    estado='COMPLETADA',
                    fecha_venta=timezone.now()
                )
                
                # Crear los detalles de la factura
                subtotal = Decimal('0.00')
                for item in productos_data:
                    producto_id = item.get('producto_id')
                    cantidad = int(item.get('cantidad', 0))
                    
                    producto = Producto.objects.get(id=producto_id)
                    precio_unitario = producto.precio_venta
                    subtotal_item = Decimal(str(cantidad)) * precio_unitario
                    subtotal += subtotal_item
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        subtotal=subtotal_item
                    )
                
                # Actualizar totales de la factura
                factura.subtotal = subtotal
                factura.total = subtotal - descuento
                factura.save()
            
            messages.success(
                request, 
                f'Factura #{factura.numero_factura} creada exitosamente. Total: C$ {factura.total:.2f}'
            )
            return redirect('facturacion:detalle', factura_id=factura.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear la factura: {str(e)}')
            return redirect('facturacion:nueva')
    
    # GET: Mostrar formulario
    form = FacturaForm()
    productos = Producto.objects.filter(activo=True, stock_actual__gt=0).order_by('nombre')
    
    context = {
        'form': form,
        'productos': productos,
        'numero_factura': generar_numero_factura(),
    }
    
    return render(request, 'facturacion/nueva.html', context)


@login_required
def obtener_producto(request, producto_id):
    """
    API endpoint para obtener información de un producto (JSON).
    """
    try:
        producto = Producto.objects.get(id=producto_id, activo=True)
        return JsonResponse({
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'precio_venta': float(producto.precio_venta),
            'stock_actual': producto.stock_actual,
            'unidad_medida': producto.unidad_medida,
        })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


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


@login_required
def anular_factura(request, factura_id):
    """
    Anular una factura (restaura el stock automáticamente).
    """
    factura = get_object_or_404(Factura, id=factura_id)
    
    if factura.estado == 'ANULADA':
        messages.warning(request, 'Esta factura ya está anulada.')
        return redirect('facturacion:detalle', factura_id=factura.id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                factura.estado = 'ANULADA'
                factura.save()
            
            messages.success(request, f'Factura #{factura.numero_factura} anulada exitosamente. El stock ha sido restaurado.')
            return redirect('facturacion:detalle', factura_id=factura.id)
        except Exception as e:
            messages.error(request, f'Error al anular la factura: {str(e)}')
            return redirect('facturacion:detalle', factura_id=factura.id)
    
    # GET: Mostrar confirmación
    context = {
        'factura': factura,
    }
    return render(request, 'facturacion/anular.html', context)


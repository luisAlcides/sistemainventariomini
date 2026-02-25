"""
Vistas para el módulo de inventario.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F, Sum
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import json

from inventario.models import Producto, Categoria, EntradaCompra, DetalleEntradaCompra, AjusteInventario
from .forms import ProductoForm, CategoriaForm, EntradaCompraForm, AjusteInventarioForm
from reportes.views import obtener_complementarios_para_producto


@login_required
def index(request):
    """
    Dashboard de inventario.
    """
    total_productos = Producto.objects.filter(activo=True).count()
    productos_por_agotarse = Producto.objects.filter(
        activo=True
    ).filter(
        stock_actual__lte=F('stock_minimo')
    ).count()
    
    productos_bajo_stock = Producto.objects.filter(
        activo=True
    ).filter(
        stock_actual__lte=F('stock_minimo')
    )[:10]
    
    # Productos próximos a expirar (en los próximos 30 días)
    fecha_limite = timezone.now().date() + timedelta(days=30)
    productos_por_expirar = Producto.objects.filter(
        activo=True,
        fecha_expiracion__isnull=False,
        fecha_expiracion__lte=fecha_limite
    ).count()
    
    productos_proximos_expirar = Producto.objects.filter(
        activo=True,
        fecha_expiracion__isnull=False,
        fecha_expiracion__lte=fecha_limite
    ).order_by('fecha_expiracion')[:10]
    
    context = {
        'total_productos': total_productos,
        'productos_por_agotarse': productos_por_agotarse,
        'productos_bajo_stock': productos_bajo_stock,
        'productos_por_expirar': productos_por_expirar,
        'productos_proximos_expirar': productos_proximos_expirar,
    }
    
    return render(request, 'inventario/index.html', context)


@login_required
def lista_productos(request):
    """
    Lista de productos.
    """
    productos = Producto.objects.all().order_by('nombre_producto__nombre')
    
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')
    
    if query:
        productos = productos.filter(
            Q(nombre_producto__nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if estado == 'activo':
        productos = productos.filter(activo=True)
    elif estado == 'inactivo':
        productos = productos.filter(activo=False)
    elif estado == 'por_agotarse':
        productos = productos.filter(activo=True, stock_actual__lte=F('stock_minimo'))
    
    categorias = Categoria.objects.filter(activa=True)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_selected': categoria_id,
        'estado_selected': estado,
    }
    
    return render(request, 'inventario/productos.html', context)


@login_required
def crear_producto(request):
    """
    Crear un nuevo producto.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('inventario:productos')
    else:
        form = ProductoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Producto',
    }
    
    return render(request, 'inventario/producto_form.html', context)


@login_required
def editar_producto(request, producto_id):
    """
    Editar un producto existente.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('inventario:productos')
    else:
        form = ProductoForm(instance=producto)
    
    context = {
        'form': form,
        'producto': producto,
        'titulo': f'Editar Producto: {producto.nombre}',
    }
    
    return render(request, 'inventario/producto_form.html', context)


@login_required
def detalle_producto(request, producto_id):
    """
    Ver detalle de un producto.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    complementarios = obtener_complementarios_para_producto(producto.id, limite=5)
    
    context = {
        'producto': producto,
        'complementarios': complementarios,
    }
    
    return render(request, 'inventario/detalle_producto.html', context)


@login_required
def productos_por_agotarse(request):
    """
    Lista de productos por agotarse.
    """
    productos = Producto.objects.filter(
        activo=True
    ).filter(
        stock_actual__lte=F('stock_minimo')
    ).order_by('stock_actual')
    
    context = {
        'productos': productos,
    }
    
    return render(request, 'inventario/productos_por_agotarse.html', context)


@login_required
def productos_por_expirar(request):
    """
    Lista de productos próximos a expirar.
    """
    # Obtener días desde parámetro (default: 30 días)
    dias = int(request.GET.get('dias', 30))
    fecha_limite = timezone.now().date() + timedelta(days=dias)
    
    productos = Producto.objects.filter(
        activo=True,
        fecha_expiracion__isnull=False,
        fecha_expiracion__lte=fecha_limite
    ).order_by('fecha_expiracion')
    
    # Separar productos expirados y próximos a expirar
    fecha_actual = timezone.now().date()
    productos_expirados = productos.filter(fecha_expiracion__lt=fecha_actual)
    productos_proximos = productos.filter(fecha_expiracion__gte=fecha_actual)
    
    context = {
        'productos': productos,
        'productos_expirados': productos_expirados,
        'productos_proximos': productos_proximos,
        'dias': dias,
    }
    
    return render(request, 'inventario/productos_por_expirar.html', context)


@login_required
def lista_entradas(request):
    """
    Lista de entradas de compra.
    """
    entradas = EntradaCompra.objects.all().order_by('-fecha_compra')[:50]
    
    context = {
        'entradas': entradas,
    }
    
    return render(request, 'inventario/entradas.html', context)


@login_required
def nueva_entrada(request):
    """
    Registrar nueva entrada de compra con múltiples productos.
    """
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            numero_factura = request.POST.get('numero_factura', '').strip()
            proveedor = request.POST.get('proveedor', '').strip()
            fecha_compra = request.POST.get('fecha_compra')
            observaciones = request.POST.get('observaciones', '').strip()
            
            # Obtener productos del JSON
            productos_json = request.POST.get('productos', '[]')
            productos_data = json.loads(productos_json)
            
            if not productos_data:
                messages.error(request, 'Debe agregar al menos un producto a la entrada.')
                return redirect('inventario:entrada_nueva')
            
            if not numero_factura or not proveedor:
                messages.error(request, 'Debe completar el número de factura y el proveedor.')
                return redirect('inventario:entrada_nueva')
            
            # Crear entrada con transacción
            with transaction.atomic():
                entrada = EntradaCompra.objects.create(
                    numero_factura=numero_factura,
                    proveedor_id=int(proveedor) if proveedor.isdigit() else None,
                    fecha_compra=fecha_compra or timezone.now().date(),
                    observaciones=observaciones,
                    usuario_registro=request.user
                )
                
                # Crear los detalles de la entrada
                from decimal import Decimal
                total = Decimal('0.00')
                for item in productos_data:
                    producto_id = item.get('producto_id')
                    cantidad = int(item.get('cantidad', 0))
                    precio_unitario = Decimal(str(item.get('precio_unitario') or item.get('precio', 0)))
                    fecha_vencimiento = item.get('fecha_vencimiento') or None
                    
                    producto = Producto.objects.get(id=producto_id)
                    subtotal = Decimal(str(cantidad)) * precio_unitario
                    total += subtotal
                    
                    DetalleEntradaCompra.objects.create(
                        entrada_compra=entrada,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        subtotal=subtotal,
                        fecha_vencimiento=fecha_vencimiento
                    )
                    
                    # Actualizar fecha de expiración del producto si la nueva es más reciente o el producto no tiene
                    if fecha_vencimiento:
                        if not producto.fecha_expiracion or fecha_vencimiento < str(producto.fecha_expiracion):
                            producto.fecha_expiracion = fecha_vencimiento
                            producto.save(update_fields=['fecha_expiracion'])
                
                # Actualizar total de la entrada
                entrada.total = total
                entrada.save()
            
            messages.success(
                request, 
                f'Entrada de compra #{entrada.id} registrada exitosamente. Total: C$ {entrada.total:.2f}'
            )
            return redirect('inventario:detalle_entrada', entrada_id=entrada.id)
            
        except Exception as e:
            messages.error(request, f'Error al registrar la entrada: {str(e)}')
            return redirect('inventario:entrada_nueva')
    
    # GET: Mostrar formulario
    form = EntradaCompraForm(initial={'fecha_compra': timezone.now().date()})
    productos = Producto.objects.filter(activo=True).order_by('nombre_producto__nombre')
    
    context = {
        'form': form,
        'productos': productos,
    }
    
    return render(request, 'inventario/nueva_entrada.html', context)


@login_required
def detalle_entrada(request, entrada_id):
    """
    Ver detalle de una entrada de compra.
    """
    entrada = get_object_or_404(EntradaCompra, id=entrada_id)
    detalles = entrada.detalles.all()
    
    context = {
        'entrada': entrada,
        'detalles': detalles,
    }
    
    return render(request, 'inventario/detalle_entrada.html', context)


@login_required
def lista_ajustes(request):
    """
    Lista de ajustes de inventario.
    """
    ajustes = AjusteInventario.objects.all().order_by('-fecha_ajuste')[:50]
    
    # Filtros
    tipo = request.GET.get('tipo', '')
    producto_id = request.GET.get('producto', '')
    
    if tipo:
        ajustes = ajustes.filter(tipo_ajuste=tipo)
    
    if producto_id:
        ajustes = ajustes.filter(producto_id=producto_id)
    
    context = {
        'ajustes': ajustes,
        'tipo_selected': tipo,
        'producto_selected': producto_id,
    }
    
    return render(request, 'inventario/ajustes.html', context)


@login_required
def crear_ajuste(request):
    """
    Crear un nuevo ajuste de inventario.
    """
    if request.method == 'POST':
        form = AjusteInventarioForm(request.POST)
        if form.is_valid():
            ajuste = form.save(commit=False)
            
            # Obtener el stock actual del producto
            producto = ajuste.producto
            ajuste.cantidad_anterior = producto.stock_actual
            ajuste.diferencia = ajuste.cantidad_nueva - ajuste.cantidad_anterior
            ajuste.usuario_registro = request.user
            ajuste.fecha_ajuste = timezone.now()
            
            ajuste.save()
            
            messages.success(
                request, 
                f'Ajuste de inventario creado exitosamente. Stock actualizado de {ajuste.cantidad_anterior} a {ajuste.cantidad_nueva}.'
            )
            return redirect('inventario:ajustes')
    else:
        form = AjusteInventarioForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Ajuste de Inventario',
    }
    
    return render(request, 'inventario/ajuste_form.html', context)


@login_required
def obtener_nombre_producto_info(request, nombre_producto_id):
    """
    API endpoint para obtener información de un nombre de producto (JSON).
    """
    try:
        nombre_producto = NombreProducto.objects.get(id=nombre_producto_id, activo=True)
        return JsonResponse({
            'id': nombre_producto.id,
            'nombre': nombre_producto.nombre,
            'categoria_id': nombre_producto.categoria.id,
            'unidad_medida': nombre_producto.unidad_medida,
        })
    except NombreProducto.DoesNotExist:
        return JsonResponse({'error': 'Nombre de producto no encontrado'}, status=404)


@login_required
def obtener_producto_info(request, producto_id):
    """
    API endpoint para obtener información de un producto (JSON).
    """
    try:
        producto = Producto.objects.get(id=producto_id, activo=True)
        return JsonResponse({
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'precio_compra': float(producto.precio_compra),
            'stock_actual': producto.stock_actual,
            'unidad_medida': producto.unidad_medida,
        })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


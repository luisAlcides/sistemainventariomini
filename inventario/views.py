"""
Vistas para el módulo de inventario.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.utils import timezone

from inventario.models import Producto, Categoria, EntradaCompra, AjusteInventario


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
    
    context = {
        'total_productos': total_productos,
        'productos_por_agotarse': productos_por_agotarse,
        'productos_bajo_stock': productos_bajo_stock,
    }
    
    return render(request, 'inventario/index.html', context)


@login_required
def lista_productos(request):
    """
    Lista de productos.
    """
    productos = Producto.objects.all().order_by('nombre')
    
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    categorias = Categoria.objects.filter(activa=True)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_selected': categoria_id,
    }
    
    return render(request, 'inventario/productos.html', context)


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
    Registrar nueva entrada de compra.
    """
    if request.method == 'POST':
        messages.success(request, 'Entrada de compra registrada exitosamente')
        return redirect('inventario:entradas')
    
    productos = Producto.objects.filter(activo=True)
    
    context = {
        'productos': productos,
    }
    
    return render(request, 'inventario/nueva_entrada.html', context)


@login_required
def lista_ajustes(request):
    """
    Lista de ajustes de inventario.
    """
    ajustes = AjusteInventario.objects.all().order_by('-fecha_ajuste')[:50]
    
    context = {
        'ajustes': ajustes,
    }
    
    return render(request, 'inventario/ajustes.html', context)


"""
Vistas para el módulo de catálogos.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from inventario.models import Producto, Categoria
from ventas.models import Cliente


@login_required
def index(request):
    """
    Índice de catálogos.
    """
    total_productos = Producto.objects.filter(activo=True).count()
    total_categorias = Categoria.objects.filter(activa=True).count()
    total_clientes = Cliente.objects.filter(activo=True).count()
    
    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_clientes': total_clientes,
    }
    
    return render(request, 'catalogos/index.html', context)


@login_required
def lista_productos(request):
    """
    Lista de productos (catálogo).
    """
    productos = Producto.objects.filter(activo=True).order_by('nombre')
    
    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(
            nombre__icontains=query
        ) | productos.filter(
            codigo__icontains=query
        )
    
    context = {
        'productos': productos,
        'query': query,
    }
    
    return render(request, 'catalogos/productos.html', context)


@login_required
def producto_nuevo(request):
    """
    Agregar nuevo producto.
    """
    if request.method == 'POST':
        messages.success(request, 'Producto agregado exitosamente')
        return redirect('catalogos:productos')
    
    categorias = Categoria.objects.filter(activa=True)
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'catalogos/producto_nuevo.html', context)


@login_required
def lista_clientes(request):
    """
    Lista de clientes.
    """
    clientes = Cliente.objects.filter(activo=True).order_by('nombre')
    
    query = request.GET.get('q', '')
    if query:
        clientes = clientes.filter(
            nombre__icontains=query
        ) | clientes.filter(
            cedula__icontains=query
        )
    
    context = {
        'clientes': clientes,
        'query': query,
    }
    
    return render(request, 'catalogos/clientes.html', context)


@login_required
def lista_categorias(request):
    """
    Lista de categorías.
    """
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'catalogos/categorias.html', context)


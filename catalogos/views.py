"""
Vistas para el módulo de catálogos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from django.db.models import Sum
from inventario.models import Producto, Categoria, NombreProducto
from ventas.models import Cliente
from .forms import ClienteForm, ProductoCatalogForm, CategoriaCatalogForm, NombreProductoForm


@login_required
def index(request):
    """
    Índice de catálogos.
    """
    total_productos = Producto.objects.filter(activo=True).count()
    total_categorias = Categoria.objects.filter(activa=True).count()
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_nombres_productos = NombreProducto.objects.filter(activo=True).count()
    
    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_clientes': total_clientes,
        'total_nombres_productos': total_nombres_productos,
    }
    
    return render(request, 'catalogos/index.html', context)


@login_required
def lista_productos(request):
    """
    Lista de productos (catálogo).
    """
    productos = Producto.objects.filter(activo=True).order_by('nombre_producto__nombre')
    
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    
    if query:
        productos = productos.filter(
            Q(nombre_producto__nombre__icontains=query) |
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
    
    return render(request, 'catalogos/productos.html', context)


@login_required
def producto_nuevo(request):
    """
    Agregar nuevo producto desde catálogos.
    """
    if request.method == 'POST':
        form = ProductoCatalogForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" agregado exitosamente.')
            return redirect('catalogos:productos')
    else:
        form = ProductoCatalogForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Producto',
    }
    
    return render(request, 'catalogos/producto_form.html', context)


@login_required
def producto_editar(request, producto_id):
    """
    Editar un producto existente desde catálogos.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ProductoCatalogForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('catalogos:productos')
    else:
        form = ProductoCatalogForm(instance=producto)
    
    context = {
        'form': form,
        'producto': producto,
        'titulo': f'Editar Producto: {producto.nombre}',
    }
    
    return render(request, 'catalogos/producto_form.html', context)


@login_required
def producto_detalle(request, producto_id):
    """
    Ver detalle de un producto desde catálogos.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    
    context = {
        'producto': producto,
    }
    
    return render(request, 'catalogos/producto_detalle.html', context)


@login_required
def lista_clientes(request):
    """
    Lista de clientes.
    """
    clientes = Cliente.objects.all().order_by('nombre')
    
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    
    if query:
        clientes = clientes.filter(
            Q(nombre_producto__nombre__icontains=query) |
            Q(cedula__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )
    
    if tipo:
        clientes = clientes.filter(tipo_cliente=tipo)
    
    if estado == 'activo':
        clientes = clientes.filter(activo=True)
    elif estado == 'inactivo':
        clientes = clientes.filter(activo=False)
    
    context = {
        'clientes': clientes,
        'query': query,
        'tipo_selected': tipo,
        'estado_selected': estado,
    }
    
    return render(request, 'catalogos/clientes.html', context)


@login_required
def cliente_nuevo(request):
    """
    Crear un nuevo cliente.
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente.')
            return redirect('catalogos:clientes')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Cliente',
    }
    
    return render(request, 'catalogos/cliente_form.html', context)


@login_required
def cliente_editar(request, cliente_id):
    """
    Editar un cliente existente.
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" actualizado exitosamente.')
            return redirect('catalogos:clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'titulo': f'Editar Cliente: {cliente.nombre}',
    }
    
    return render(request, 'catalogos/cliente_form.html', context)


@login_required
def cliente_detalle(request, cliente_id):
    """
    Ver detalle de un cliente.
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    # Obtener facturas del cliente
    facturas = cliente.facturas.all().order_by('-fecha_venta')[:10]
    total_facturas = cliente.facturas.count()
    total_compras = cliente.facturas.aggregate(
        total=Sum('total')
    )['total'] or 0
    
    context = {
        'cliente': cliente,
        'facturas': facturas,
        'total_facturas': total_facturas,
        'total_compras': total_compras,
    }
    
    return render(request, 'catalogos/cliente_detalle.html', context)


@login_required
def lista_categorias(request):
    """
    Lista de categorías.
    """
    categorias = Categoria.objects.all().order_by('nombre')
    
    estado = request.GET.get('estado', '')
    if estado == 'activa':
        categorias = categorias.filter(activa=True)
    elif estado == 'inactiva':
        categorias = categorias.filter(activa=False)
    
    context = {
        'categorias': categorias,
        'estado_selected': estado,
    }
    
    return render(request, 'catalogos/categorias.html', context)


@login_required
def categoria_nueva(request):
    """
    Crear una nueva categoría.
    """
    if request.method == 'POST':
        form = CategoriaCatalogForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return redirect('catalogos:categorias')
    else:
        form = CategoriaCatalogForm()
    
    context = {
        'form': form,
        'titulo': 'Nueva Categoría',
    }
    
    return render(request, 'catalogos/categoria_form.html', context)


@login_required
def categoria_editar(request, categoria_id):
    """
    Editar una categoría existente.
    """
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaCatalogForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente.')
            return redirect('catalogos:categorias')
    else:
        form = CategoriaCatalogForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'titulo': f'Editar Categoría: {categoria.nombre}',
    }
    
    return render(request, 'catalogos/categoria_form.html', context)


# ========== NOMBRES DE PRODUCTOS ==========

@login_required
def lista_nombres_productos(request):
    """
    Lista de nombres de productos.
    """
    nombres = NombreProducto.objects.all().order_by('nombre')
    
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')
    
    if query:
        nombres = nombres.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    if categoria_id:
        nombres = nombres.filter(categoria_id=categoria_id)
    
    if estado == 'activo':
        nombres = nombres.filter(activo=True)
    elif estado == 'inactivo':
        nombres = nombres.filter(activo=False)
    
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    
    context = {
        'nombres': nombres,
        'categorias': categorias,
        'query': query,
        'categoria_selected': categoria_id,
        'estado_selected': estado,
    }
    
    return render(request, 'catalogos/nombres_productos.html', context)


@login_required
def nombre_producto_nuevo(request):
    """
    Crear nuevo nombre de producto.
    """
    if request.method == 'POST':
        form = NombreProductoForm(request.POST)
        if form.is_valid():
            nombre_producto = form.save()
            messages.success(request, f'Nombre de producto "{nombre_producto.nombre}" creado exitosamente.')
            return redirect('catalogos:nombres_productos')
    else:
        form = NombreProductoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Nombre de Producto',
    }
    
    return render(request, 'catalogos/nombre_producto_form.html', context)


@login_required
def nombre_producto_editar(request, nombre_producto_id):
    """
    Editar nombre de producto.
    """
    nombre_producto = get_object_or_404(NombreProducto, id=nombre_producto_id)
    
    if request.method == 'POST':
        form = NombreProductoForm(request.POST, instance=nombre_producto)
        if form.is_valid():
            nombre_producto = form.save()
            messages.success(request, f'Nombre de producto "{nombre_producto.nombre}" actualizado exitosamente.')
            return redirect('catalogos:nombres_productos')
    else:
        form = NombreProductoForm(instance=nombre_producto)
    
    context = {
        'form': form,
        'nombre_producto': nombre_producto,
        'titulo': f'Editar Nombre: {nombre_producto.nombre}',
    }
    
    return render(request, 'catalogos/nombre_producto_form.html', context)


@login_required
def nombre_producto_detalle(request, nombre_producto_id):
    """
    Ver detalle de nombre de producto.
    """
    nombre_producto = get_object_or_404(NombreProducto, id=nombre_producto_id)
    productos = nombre_producto.productos.filter(activo=True)
    
    context = {
        'nombre_producto': nombre_producto,
        'productos': productos,
    }
    
    return render(request, 'catalogos/nombre_producto_detalle.html', context)


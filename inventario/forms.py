"""
Formularios para el módulo de inventario.
"""
from django import forms
from inventario.models import Producto, Categoria, EntradaCompra, DetalleEntradaCompra, AjusteInventario


class ProductoForm(forms.ModelForm):
    """
    Formulario para crear/editar productos.
    """
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'descripcion', 'categoria', 
            'precio_venta', 'precio_compra', 'costo_promedio',
            'porcentaje_ganancia', 'actualizar_precio_automatico',
            'stock_actual', 'stock_minimo', 'unidad_medida', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Código único del producto'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Descripción del producto (opcional)'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.01',
                'min': '0'
            }),
            'precio_compra': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.01',
                'min': '0'
            }),
            'costo_promedio': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.01',
                'min': '0',
                'readonly': True
            }),
            'porcentaje_ganancia': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.01',
                'min': '0'
            }),
            'actualizar_precio_automatico': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'min': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'min': '0'
            }),
            'unidad_medida': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Ej: unidad, kg, litro, caja'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }
        labels = {
            'codigo': 'Código del Producto',
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'precio_venta': 'Precio de Venta (C$)',
            'precio_compra': 'Precio de Compra (C$)',
            'costo_promedio': 'Costo Promedio (C$)',
            'porcentaje_ganancia': 'Porcentaje de Ganancia (%)',
            'actualizar_precio_automatico': 'Actualizar Precio Automáticamente',
            'stock_actual': 'Stock Actual',
            'stock_minimo': 'Stock Mínimo',
            'unidad_medida': 'Unidad de Medida',
            'activo': 'Producto Activo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(activa=True).order_by('nombre')


class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear/editar categorías.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Descripción (opcional)'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
        }


class EntradaCompraForm(forms.ModelForm):
    """
    Formulario para crear entradas de compra.
    """
    class Meta:
        model = EntradaCompra
        fields = ['numero_factura', 'proveedor', 'fecha_compra', 'observaciones']
        widgets = {
            'numero_factura': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Número de factura del proveedor'
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nombre del proveedor'
            }),
            'fecha_compra': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Observaciones (opcional)'
            }),
        }
        labels = {
            'numero_factura': 'Número de Factura de Compra',
            'proveedor': 'Proveedor',
            'fecha_compra': 'Fecha de Compra',
            'observaciones': 'Observaciones',
        }


class DetalleEntradaCompraForm(forms.ModelForm):
    """
    Formulario para agregar detalles a una entrada de compra.
    """
    class Meta:
        model = DetalleEntradaCompra
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent producto-select'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': '1'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01',
                'min': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(activo=True).order_by('nombre')


class AjusteInventarioForm(forms.ModelForm):
    """
    Formulario para crear ajustes de inventario.
    """
    class Meta:
        model = AjusteInventario
        fields = ['producto', 'tipo_ajuste', 'cantidad_nueva', 'motivo']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent'
            }),
            'tipo_ajuste': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent'
            }),
            'cantidad_nueva': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'min': '0'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Motivo del ajuste (obligatorio)'
            }),
        }
        labels = {
            'producto': 'Producto',
            'tipo_ajuste': 'Tipo de Ajuste',
            'cantidad_nueva': 'Cantidad Nueva',
            'motivo': 'Motivo del Ajuste',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(activo=True).order_by('nombre')


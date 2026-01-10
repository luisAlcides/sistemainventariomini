"""
Formularios para el módulo de catálogos.
"""
from django import forms
from ventas.models import Cliente
from inventario.models import Categoria, Producto, NombreProducto
from inventario.forms import ProductoForm, CategoriaForm


class ClienteForm(forms.ModelForm):
    """
    Formulario para crear/editar clientes.
    """
    class Meta:
        model = Cliente
        fields = ['nombre', 'cedula', 'telefono', 'email', 'direccion', 'tipo_cliente', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Nombre completo del cliente'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Número de cédula (opcional)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Teléfono de contacto'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Dirección del cliente (opcional)'
            }),
            'tipo_cliente': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500'
            }),
        }
        labels = {
            'nombre': 'Nombre del Cliente',
            'cedula': 'Cédula',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
            'tipo_cliente': 'Tipo de Cliente',
            'activo': 'Cliente Activo',
        }


class NombreProductoForm(forms.ModelForm):
    """
    Formulario para crear/editar nombres de productos.
    """
    class Meta:
        model = NombreProducto
        fields = ['nombre', 'categoria', 'unidad_medida', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Nombre del producto (ej: Arroz, Azúcar, etc.)'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
            }),
            'unidad_medida': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ej: unidad, kg, litro, caja'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Descripción general del producto (opcional)'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500'
            }),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'categoria': 'Categoría',
            'unidad_medida': 'Unidad de Medida',
            'descripcion': 'Descripción General',
            'activo': 'Nombre Activo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(activa=True).order_by('nombre')


# Reutilizar formularios de inventario
ProductoCatalogForm = ProductoForm
CategoriaCatalogForm = CategoriaForm

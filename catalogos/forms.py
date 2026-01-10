"""
Formularios para el módulo de catálogos.
"""
from django import forms
from ventas.models import Cliente
from inventario.models import Categoria, Producto
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


# Reutilizar formularios de inventario
ProductoCatalogForm = ProductoForm
CategoriaCatalogForm = CategoriaForm

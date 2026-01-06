"""
Formularios para el módulo de facturación.
"""
from django import forms
from ventas.models import Factura, DetalleFactura, Cliente
from inventario.models import Producto
from ventas.utils import generar_numero_factura


class FacturaForm(forms.ModelForm):
    """
    Formulario para crear/editar una factura.
    """
    cliente_nombre = forms.CharField(
        label='Nombre del Cliente',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Nombre del cliente (si no está registrado)'
        })
    )
    
    descuento = forms.DecimalField(
        label='Descuento (C$)',
        required=False,
        initial=0,
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'step': '0.01',
            'value': '0.00'
        })
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 3,
            'placeholder': 'Observaciones adicionales...'
        })
    )
    
    class Meta:
        model = Factura
        fields = ['cliente', 'cliente_nombre', 'descuento', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
        }
        labels = {
            'cliente': 'Cliente Registrado',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo clientes activos
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True)
        self.fields['cliente'].required = False
        self.fields['cliente'].empty_label = '-- Seleccionar cliente registrado --'


class DetalleFacturaForm(forms.ModelForm):
    """
    Formulario para agregar un detalle (producto) a la factura.
    """
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True, stock_actual__gt=0),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent producto-select'
        }),
        label='Producto'
    )
    
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent cantidad-input',
            'min': '1'
        }),
        label='Cantidad'
    )
    
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar productos por nombre
        self.fields['producto'].queryset = Producto.objects.filter(
            activo=True, 
            stock_actual__gt=0
        ).order_by('nombre')
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        producto = self.cleaned_data.get('producto')
        
        if producto and cantidad:
            if cantidad > producto.stock_actual:
                raise forms.ValidationError(
                    f'Stock insuficiente. Disponible: {producto.stock_actual} unidades'
                )
        
        return cantidad


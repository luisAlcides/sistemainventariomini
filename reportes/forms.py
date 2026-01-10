"""
Formularios para filtros de reportes.
"""
from django import forms
from django.utils import timezone
from datetime import date, timedelta


class RangoFechasForm(forms.Form):
    """
    Formulario para seleccionar un rango de fechas.
    """
    fecha_inicio = forms.DateField(
        label='Fecha Inicio',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date'
        })
    )
    
    fecha_fin = forms.DateField(
        label='Fecha Fin',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Valores por defecto: últimos 30 días
        if not self.is_bound:
            hoy = date.today()
            self.fields['fecha_inicio'].initial = hoy - timedelta(days=30)
            self.fields['fecha_fin'].initial = hoy
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                raise forms.ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')
        
        return cleaned_data


class ReporteVentasForm(RangoFechasForm):
    """
    Formulario para reporte de ventas con filtros adicionales.
    """
    vendedor = forms.ChoiceField(
        label='Vendedor',
        required=False,
        choices=[('', 'Todos los vendedores')],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from usuarios.models import Usuario
        vendedores = Usuario.objects.filter(
            rol__codigo__in=['ADMIN', 'VEND']
        ).order_by('first_name', 'last_name', 'username')
        
        choices = [('', 'Todos los vendedores')]
        for vendedor in vendedores:
            nombre = vendedor.get_full_name() or vendedor.username
            choices.append((vendedor.id, nombre))
        
        self.fields['vendedor'].choices = choices

"""
Utilidades para el módulo de ventas.
"""
from django.utils import timezone
from .models import Factura


def generar_numero_factura():
    """
    Genera un número de factura único basado en la fecha y el último número secuencial del día.
    Formato: FACT-YYYYMMDD-XXXX
    """
    fecha_actual = timezone.now().date()
    fecha_str = fecha_actual.strftime('%Y%m%d')
    prefix = f"FACT-{fecha_str}-"
    
    # Buscar la última factura del día por número correlativo
    ultima_factura = Factura.objects.filter(
        numero_factura__startswith=prefix
    ).order_by('-numero_factura').first()
    
    if ultima_factura:
        # Extraer el número secuencial (últimos 4 caracteres)
        try:
            ultimo_numero = int(ultima_factura.numero_factura.split('-')[-1])
            nuevo_numero = ultimo_numero + 1
        except (ValueError, IndexError):
            nuevo_numero = 1
    else:
        nuevo_numero = 1
    
    # Generar número secuencial (4 dígitos)
    numero_secuencial = str(nuevo_numero).zfill(4)
    
    return f"{prefix}{numero_secuencial}"


def calcular_totales_factura(factura):
    """
    Calcula y actualiza los totales de una factura.
    """
    detalles = factura.detalles.all()
    subtotal = sum(detalle.subtotal for detalle in detalles)
    total = subtotal - factura.descuento
    
    factura.subtotal = subtotal
    factura.total = total
    factura.save(update_fields=['subtotal', 'total'])
    
    return subtotal, total


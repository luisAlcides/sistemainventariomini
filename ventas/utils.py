"""
Utilidades para el módulo de ventas.
"""
from django.utils import timezone
from .models import Factura


def generar_numero_factura():
    """
    Genera un número de factura único basado en la fecha y un contador.
    Formato: FACT-YYYYMMDD-XXXX
    """
    fecha_actual = timezone.now().date()
    fecha_str = fecha_actual.strftime('%Y%m%d')
    
    # Contar facturas del día
    facturas_hoy = Factura.objects.filter(
        fecha_creacion__date=fecha_actual
    ).count()
    
    # Generar número secuencial (4 dígitos)
    numero_secuencial = str(facturas_hoy + 1).zfill(4)
    
    return f"FACT-{fecha_str}-{numero_secuencial}"


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


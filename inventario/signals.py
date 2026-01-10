"""
Signals para el módulo de inventario.
Maneja la lógica de actualización de stock en entradas de compra y ajustes.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import DetalleEntradaCompra, AjusteInventario


@receiver(post_save, sender=DetalleEntradaCompra)
def aumentar_stock_al_comprar(sender, instance, created, **kwargs):
    """
    Signal que aumenta automáticamente el stock del producto cuando se registra una entrada de compra.
    También calcula el costo promedio y actualiza el precio de venta si está configurado.
    """
    if created:
        producto = instance.producto
        
        with transaction.atomic():
            # Aumentar el stock primero
            producto.stock_actual += instance.cantidad
            producto.save(update_fields=['stock_actual'])
            
            # Calcular y actualizar costo promedio (esto también guarda el producto)
            producto.actualizar_costo_promedio()


@receiver(post_save, sender=AjusteInventario)
def aplicar_ajuste_inventario(sender, instance, created, **kwargs):
    """
    Signal que actualiza el stock del producto cuando se crea un ajuste de inventario manual.
    Evita actualizar si el stock ya fue modificado (ajustes automáticos desde otros signals).
    """
    if created:
        producto = instance.producto
        
        # Solo actualizar si el stock actual no coincide con la cantidad nueva
        # Esto evita actualizaciones duplicadas cuando el ajuste es automático
        if producto.stock_actual != instance.cantidad_nueva:
            with transaction.atomic():
                # Actualizar el stock con la cantidad nueva del ajuste
                producto.stock_actual = instance.cantidad_nueva
                producto.save(update_fields=['stock_actual'])

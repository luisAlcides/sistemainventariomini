"""
Signals para el módulo de ventas.
Maneja la lógica de descuento automático de stock al facturar.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import DetalleFactura, Factura
from inventario.models import AjusteInventario


@receiver(post_save, sender=DetalleFactura)
def descontar_stock_al_facturar(sender, instance, created, **kwargs):
    """
    Signal que descuenta automáticamente el stock del producto cuando se crea un detalle de factura.
    Solo se ejecuta cuando se crea un nuevo detalle (created=True).
    """
    if created and instance.factura.estado == 'COMPLETADA':
        producto = instance.producto
        
        # Verificar que hay stock suficiente
        if not producto.tiene_stock_suficiente(instance.cantidad):
            raise ValueError(
                f"No hay stock suficiente para {producto.nombre}. "
                f"Stock disponible: {producto.stock_actual}, "
                f"Cantidad solicitada: {instance.cantidad}"
            )
        
        # Descontar el stock
        with transaction.atomic():
            producto.stock_actual -= instance.cantidad
            producto.save(update_fields=['stock_actual'])
            
            # Registrar un ajuste de inventario automático
            AjusteInventario.objects.create(
                producto=producto,
                tipo_ajuste='SALIDA',
                cantidad_anterior=producto.stock_actual + instance.cantidad,
                cantidad_nueva=producto.stock_actual,
                diferencia=-instance.cantidad,
                motivo=f'Venta - Factura #{instance.factura.numero_factura}',
                usuario_registro=instance.factura.vendedor
            )


@receiver(post_delete, sender=DetalleFactura)
def restaurar_stock_al_eliminar_detalle(sender, instance, **kwargs):
    """
    Signal que restaura el stock cuando se elimina un detalle de factura.
    Útil para casos de anulación de facturas o correcciones.
    """
    if instance.factura.estado == 'COMPLETADA':
        producto = instance.producto
        
        with transaction.atomic():
            # Restaurar el stock
            producto.stock_actual += instance.cantidad
            producto.save(update_fields=['stock_actual'])
            
            # Registrar un ajuste de inventario automático
            AjusteInventario.objects.create(
                producto=producto,
                tipo_ajuste='ENTRADA',
                cantidad_anterior=producto.stock_actual - instance.cantidad,
                cantidad_nueva=producto.stock_actual,
                diferencia=instance.cantidad,
                motivo=f'Anulación/Corrección - Factura #{instance.factura.numero_factura}',
                usuario_registro=instance.factura.vendedor
            )


@receiver(post_save, sender=Factura)
def manejar_anulacion_factura(sender, instance, created, **kwargs):
    """
    Signal que maneja la anulación de facturas, restaurando el stock.
    Nota: Este signal se ejecuta cuando se cambia el estado a ANULADA.
    El stock se restaura automáticamente cuando se eliminan los detalles (post_delete).
    """
    # Este signal se mantiene por si se necesita lógica adicional al anular
    # El stock se restaura mediante el signal post_delete de DetalleFactura
    pass


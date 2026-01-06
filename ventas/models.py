"""
Modelos para la gestión de ventas y facturación del sistema.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from usuarios.models import Usuario
from inventario.models import Producto


class Cliente(models.Model):
    """
    Modelo para los clientes del sistema.
    """
    TIPO_CLIENTE_CHOICES = [
        ('REGULAR', 'Cliente Regular'),
        ('FRECUENTE', 'Cliente Frecuente'),
        ('MAYORISTA', 'Cliente Mayorista'),
    ]
    
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre del Cliente'
    )
    cedula = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Cédula',
        help_text='Cédula de identidad (opcional)'
    )
    telefono = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Correo Electrónico'
    )
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    tipo_cliente = models.CharField(
        max_length=20,
        choices=TIPO_CLIENTE_CHOICES,
        default='REGULAR',
        verbose_name='Tipo de Cliente'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Cliente Activo'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['cedula']),
            models.Index(fields=['activo']),
        ]
    
    def __str__(self):
        return self.nombre


class Factura(models.Model):
    """
    Modelo para las facturas de venta.
    """
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('ANULADA', 'Anulada'),
    ]
    
    numero_factura = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número de Factura',
        help_text='Número único de factura'
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='facturas',
        verbose_name='Cliente',
        null=True,
        blank=True,
        help_text='Cliente puede ser null para ventas al contado sin registro'
    )
    cliente_nombre = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Nombre del Cliente (si no está registrado)',
        help_text='Para ventas al contado sin cliente registrado'
    )
    vendedor = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='facturas_vendidas',
        verbose_name='Vendedor'
    )
    fecha_venta = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de Venta'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Subtotal (C$)',
        default=0
    )
    descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Descuento (C$)',
        default=0
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Total (C$)',
        default=0
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='COMPLETADA',
        verbose_name='Estado'
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_venta', '-fecha_creacion']
        indexes = [
            models.Index(fields=['numero_factura']),
            models.Index(fields=['fecha_venta']),
            models.Index(fields=['estado']),
            models.Index(fields=['vendedor']),
        ]
    
    def __str__(self):
        cliente_str = self.cliente.nombre if self.cliente else (self.cliente_nombre or 'Cliente General')
        return f"Factura #{self.numero_factura} - {cliente_str} ({self.fecha_venta.date()})"
    
    def calcular_totales(self):
        """Calcula los totales de la factura basándose en los detalles."""
        detalles = self.detalles.all()
        self.subtotal = sum(detalle.subtotal for detalle in detalles)
        self.total = self.subtotal - self.descuento
        self.save(update_fields=['subtotal', 'total'])


class DetalleFactura(models.Model):
    """
    Modelo para los detalles de cada factura (productos vendidos).
    """
    factura = models.ForeignKey(
        Factura,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Factura'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='ventas',
        verbose_name='Producto'
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad'
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio Unitario (C$)',
        help_text='Precio al momento de la venta'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Subtotal (C$)'
    )
    
    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Facturas'
        unique_together = ['factura', 'producto']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades - Factura #{self.factura.numero_factura}"
    
    def save(self, *args, **kwargs):
        """Calcula el subtotal automáticamente."""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar totales de la factura
        self.factura.calcular_totales()
    
    def delete(self, *args, **kwargs):
        """Al eliminar un detalle, actualiza los totales de la factura."""
        factura = self.factura
        super().delete(*args, **kwargs)
        factura.calcular_totales()


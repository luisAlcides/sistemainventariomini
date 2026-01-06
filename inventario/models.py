"""
Modelos para la gestión de inventario del sistema.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from usuarios.models import Usuario


class Categoria(models.Model):
    """
    Modelo para categorizar los productos.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre de la Categoría'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    activa = models.BooleanField(
        default=True,
        verbose_name='Categoría Activa'
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
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Modelo para los productos del inventario.
    """
    codigo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Código del Producto',
        help_text='Código único del producto (SKU, código de barras, etc.)'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre del Producto'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Categoría'
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio de Venta (C$)',
        help_text='Precio en Córdobas Nicaragüenses'
    )
    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio de Compra (C$)',
        help_text='Precio de compra en Córdobas Nicaragüenses'
    )
    stock_actual = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock Actual',
        help_text='Cantidad disponible en inventario'
    )
    stock_minimo = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock Mínimo',
        help_text='Cantidad mínima antes de alertar'
    )
    unidad_medida = models.CharField(
        max_length=20,
        default='unidad',
        verbose_name='Unidad de Medida',
        help_text='Ej: unidad, kg, litro, caja, etc.'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Producto Activo'
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
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['categoria']),
            models.Index(fields=['activo']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
    def esta_por_agotarse(self):
        """Verifica si el producto está por agotarse (stock <= stock_minimo)."""
        return self.stock_actual <= self.stock_minimo
    
    def tiene_stock_suficiente(self, cantidad):
        """Verifica si hay stock suficiente para la cantidad solicitada."""
        return self.stock_actual >= cantidad
    
    def calcular_valor_inventario(self):
        """Calcula el valor total del inventario de este producto."""
        return self.stock_actual * self.precio_compra


class EntradaCompra(models.Model):
    """
    Modelo para registrar las entradas de productos al inventario (compras).
    """
    numero_factura = models.CharField(
        max_length=50,
        verbose_name='Número de Factura de Compra',
        help_text='Número de factura del proveedor'
    )
    proveedor = models.CharField(
        max_length=200,
        verbose_name='Proveedor'
    )
    fecha_compra = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Compra'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Total (C$)',
        default=0
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones'
    )
    usuario_registro = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='entradas_compra',
        verbose_name='Usuario que Registró'
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
        verbose_name = 'Entrada/Compra'
        verbose_name_plural = 'Entradas/Compras'
        ordering = ['-fecha_compra', '-fecha_creacion']
    
    def __str__(self):
        return f"Compra #{self.id} - {self.proveedor} ({self.fecha_compra})"


class DetalleEntradaCompra(models.Model):
    """
    Modelo para los detalles de cada entrada/compra.
    """
    entrada_compra = models.ForeignKey(
        EntradaCompra,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Entrada/Compra'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='entradas_compra',
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
        verbose_name='Precio Unitario (C$)'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Subtotal (C$)'
    )
    
    class Meta:
        verbose_name = 'Detalle de Entrada/Compra'
        verbose_name_plural = 'Detalles de Entradas/Compras'
        unique_together = ['entrada_compra', 'producto']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
    
    def save(self, *args, **kwargs):
        """Calcula el subtotal automáticamente."""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)


class AjusteInventario(models.Model):
    """
    Modelo para registrar ajustes de inventario (inventarios físicos, correcciones, etc.).
    """
    TIPO_AJUSTE_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('CORRECCION', 'Corrección'),
    ]
    
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='ajustes',
        verbose_name='Producto'
    )
    tipo_ajuste = models.CharField(
        max_length=20,
        choices=TIPO_AJUSTE_CHOICES,
        verbose_name='Tipo de Ajuste'
    )
    cantidad_anterior = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad Anterior'
    )
    cantidad_nueva = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad Nueva'
    )
    diferencia = models.IntegerField(
        verbose_name='Diferencia',
        help_text='Diferencia calculada automáticamente'
    )
    motivo = models.TextField(
        verbose_name='Motivo del Ajuste'
    )
    usuario_registro = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='ajustes_inventario',
        verbose_name='Usuario que Registró'
    )
    fecha_ajuste = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha del Ajuste'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Ajuste de Inventario'
        verbose_name_plural = 'Ajustes de Inventario'
        ordering = ['-fecha_ajuste', '-fecha_creacion']
    
    def __str__(self):
        return f"Ajuste {self.tipo_ajuste} - {self.producto.nombre} ({self.fecha_ajuste})"
    
    def save(self, *args, **kwargs):
        """Calcula la diferencia automáticamente."""
        self.diferencia = self.cantidad_nueva - self.cantidad_anterior
        super().save(*args, **kwargs)


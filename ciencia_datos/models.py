"""
Modelos para el módulo de Ciencia de Datos.
Registra logs de productos recomendados generados por modelos de Machine Learning.
"""
from django.db import models
from django.utils import timezone
from inventario.models import Producto
from usuarios.models import Usuario


class ProductosRecomendados(models.Model):
    """
    Modelo para registrar logs de productos recomendados generados por ML.
    """
    TIPO_RECOMENDACION_CHOICES = [
        ('VENTA_CRUZADA', 'Venta Cruzada'),
        ('PRODUCTOS_POPULARES', 'Productos Populares'),
        ('PRODUCTOS_SIMILARES', 'Productos Similares'),
        ('PRODUCTOS_FRECUENTES', 'Productos Frecuentes del Cliente'),
        ('PREDICCION_DEMANDA', 'Predicción de Demanda'),
    ]
    
    producto_base = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='recomendaciones_como_base',
        verbose_name='Producto Base',
        help_text='Producto que generó la recomendación',
        null=True,
        blank=True
    )
    producto_recomendado = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='recomendaciones',
        verbose_name='Producto Recomendado'
    )
    tipo_recomendacion = models.CharField(
        max_length=50,
        choices=TIPO_RECOMENDACION_CHOICES,
        verbose_name='Tipo de Recomendación'
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        verbose_name='Score de Recomendación',
        help_text='Puntuación de confianza del modelo (0-1)'
    )
    contexto = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Contexto',
        help_text='Información adicional del contexto de la recomendación'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        related_name='recomendaciones_recibidas',
        verbose_name='Usuario',
        null=True,
        blank=True,
        help_text='Usuario al que se mostró la recomendación'
    )
    mostrado = models.BooleanField(
        default=False,
        verbose_name='Mostrado',
        help_text='Indica si la recomendación fue mostrada al usuario'
    )
    aceptado = models.BooleanField(
        default=False,
        verbose_name='Aceptado',
        help_text='Indica si el usuario aceptó/compró el producto recomendado'
    )
    fecha_recomendacion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de Recomendación'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Producto Recomendado'
        verbose_name_plural = 'Productos Recomendados'
        ordering = ['-fecha_recomendacion', '-score']
        indexes = [
            models.Index(fields=['producto_recomendado']),
            models.Index(fields=['tipo_recomendacion']),
            models.Index(fields=['fecha_recomendacion']),
            models.Index(fields=['score']),
            models.Index(fields=['aceptado']),
        ]
    
    def __str__(self):
        base_str = f"Basado en: {self.producto_base.nombre}" if self.producto_base else "Recomendación General"
        return f"{self.producto_recomendado.nombre} ({self.tipo_recomendacion}) - Score: {self.score}"
    
    def marcar_como_mostrado(self):
        """Marca la recomendación como mostrada."""
        self.mostrado = True
        self.save(update_fields=['mostrado'])
    
    def marcar_como_aceptado(self):
        """Marca la recomendación como aceptada (usuario compró el producto)."""
        self.aceptado = True
        self.save(update_fields=['aceptado'])


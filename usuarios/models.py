"""
Modelos para la gestión de usuarios y roles del sistema.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class Rol(models.Model):
    """
    Modelo para definir los roles del sistema.
    """
    ADMINISTRADOR = 'ADMIN'
    VENDEDOR = 'VEND'
    BODEGUERO = 'BODEG'
    
    ROL_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (VENDEDOR, 'Vendedor'),
        (BODEGUERO, 'Bodeguero'),
    ]
    
    codigo = models.CharField(
        max_length=10,
        choices=ROL_CHOICES,
        unique=True,
        verbose_name='Código de Rol'
    )
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre del Rol'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
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
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['codigo']
    
    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{8,15}$',
        message="El número de teléfono debe tener entre 8 y 15 dígitos."
    )
    
    # Campos adicionales
    cedula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Cédula',
        help_text='Número de cédula de identidad'
    )
    telefono = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name='usuarios',
        verbose_name='Rol',
        null=True,
        blank=True
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Usuario Activo'
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
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    def es_administrador(self):
        """Verifica si el usuario es administrador."""
        return self.rol and self.rol.codigo == Rol.ADMINISTRADOR
    
    def es_vendedor(self):
        """Verifica si el usuario es vendedor."""
        return self.rol and self.rol.codigo == Rol.VENDEDOR
    
    def es_bodeguero(self):
        """Verifica si el usuario es bodeguero."""
        return self.rol and self.rol.codigo == Rol.BODEGUERO
    
    def tiene_permiso_ventas(self):
        """Verifica si el usuario tiene permisos para realizar ventas."""
        return self.es_administrador() or self.es_vendedor()
    
    def tiene_permiso_inventario(self):
        """Verifica si el usuario tiene permisos para gestionar inventario."""
        return self.es_administrador() or self.es_bodeguero()


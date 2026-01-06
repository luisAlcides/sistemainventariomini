"""
Signals para el modelo Usuario.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Rol


@receiver(post_save, sender=Usuario)
def asignar_rol_por_defecto(sender, instance, created, **kwargs):
    """
    Asigna un rol por defecto si el usuario no tiene uno asignado.
    """
    if created and not instance.rol:
        # Intentar obtener el rol de Vendedor por defecto
        rol_vendedor, _ = Rol.objects.get_or_create(
            codigo=Rol.VENDEDOR,
            defaults={
                'nombre': 'Vendedor',
                'descripcion': 'Rol de vendedor por defecto'
            }
        )
        instance.rol = rol_vendedor
        instance.save(update_fields=['rol'])


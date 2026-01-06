"""
Comando de gestión para crear los roles iniciales del sistema.
Uso: python manage.py crear_roles_iniciales
"""
from django.core.management.base import BaseCommand
from usuarios.models import Rol


class Command(BaseCommand):
    help = 'Crea los roles iniciales del sistema (Administrador, Vendedor, Bodeguero)'

    def handle(self, *args, **options):
        roles_data = [
            {
                'codigo': Rol.ADMINISTRADOR,
                'nombre': 'Administrador',
                'descripcion': 'Rol con acceso completo al sistema. Puede gestionar usuarios, inventario, ventas y configuraciones.'
            },
            {
                'codigo': Rol.VENDEDOR,
                'nombre': 'Vendedor',
                'descripcion': 'Rol para realizar ventas y facturación. Acceso limitado a inventario y reportes de ventas.'
            },
            {
                'codigo': Rol.BODEGUERO,
                'nombre': 'Bodeguero',
                'descripcion': 'Rol para gestionar inventario, entradas de compra y ajustes de stock.'
            },
        ]
        
        creados = 0
        actualizados = 0
        
        for rol_data in roles_data:
            rol, created = Rol.objects.update_or_create(
                codigo=rol_data['codigo'],
                defaults={
                    'nombre': rol_data['nombre'],
                    'descripcion': rol_data['descripcion'],
                    'activo': True
                }
            )
            
            if created:
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol creado: {rol.nombre}')
                )
            else:
                actualizados += 1
                self.stdout.write(
                    self.style.WARNING(f'→ Rol actualizado: {rol.nombre}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Proceso completado: {creados} roles creados, {actualizados} roles actualizados.'
            )
        )


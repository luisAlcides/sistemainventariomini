from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Rol


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'codigo']
    search_fields = ['nombre', 'codigo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ['username', 'cedula', 'email', 'rol', 'activo', 'fecha_creacion']
    list_filter = ['rol', 'activo', 'is_staff', 'is_superuser']
    search_fields = ['username', 'cedula', 'email', 'first_name', 'last_name']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'last_login', 'date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Personal Adicional', {
            'fields': ('cedula', 'telefono', 'direccion', 'rol', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Personal', {
            'fields': ('cedula', 'telefono', 'direccion', 'rol')
        }),
    )


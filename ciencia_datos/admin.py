from django.contrib import admin
from .models import ProductosRecomendados


@admin.register(ProductosRecomendados)
class ProductosRecomendadosAdmin(admin.ModelAdmin):
    list_display = [
        'producto_recomendado',
        'producto_base',
        'tipo_recomendacion',
        'score',
        'mostrado',
        'aceptado',
        'fecha_recomendacion'
    ]
    list_filter = [
        'tipo_recomendacion',
        'mostrado',
        'aceptado',
        'fecha_recomendacion'
    ]
    search_fields = [
        'producto_recomendado__nombre',
        'producto_recomendado__codigo',
        'producto_base__nombre',
        'producto_base__codigo'
    ]
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha_recomendacion'
    
    fieldsets = (
        ('Productos', {
            'fields': ('producto_base', 'producto_recomendado')
        }),
        ('Recomendación', {
            'fields': ('tipo_recomendacion', 'score', 'contexto')
        }),
        ('Interacción', {
            'fields': ('usuario', 'mostrado', 'aceptado')
        }),
        ('Fechas', {
            'fields': ('fecha_recomendacion', 'fecha_creacion')
        }),
    )

